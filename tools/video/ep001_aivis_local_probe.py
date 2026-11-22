#!/usr/bin/env python3
"""EP001 PR #29 G1-approved A provisional AivisSpeech voice probe.

Use a LOCAL AivisSpeech Engine. This does not approve model rights or publish audio.
"""
import argparse
import csv
import io
import json
import math
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

SOURCE_PR = 'https://github.com/kouta1029/animation/pull/29'
SOURCE_SHA = '7a349c981767f609124884f0ebe063899412d428'
VOICES = {
    'protagonist': {'name': 'にせ', 'speaker_uuid': 'bf56410a-d8e6-430d-a477-f789e16206d3', 'style': 'ノーマル', 'model_uuid': '6d11c6c2-f4a4-4435-887e-23dd60f8b8dd'},
    'organizer': {'name': 'M2', 'speaker_uuid': '6c831a4b-a90c-4a88-9083-b473c25f69ec', 'style': 'ノーマル', 'model_uuid': 'd1a7446f-230d-4077-afdf-923eddabe53c'},
}
# Exact line_id + speaker + text in G1-approved PR #29, NOT PR #30.
LINES = [
    {'id': 'L01', 'speaker': 'protagonist', 'text': '近っ', 'start': 7.1, 'end': 7.9},
    {'id': 'L02', 'speaker': 'protagonist', 'text': 'ちゃんと断ろ', 'start': 17.8, 'end': 19.1},
    {'id': 'L03', 'speaker': 'organizer', 'text': 'お、来た', 'start': 37.4, 'end': 38.6},
    {'id': 'L04', 'speaker': 'organizer', 'text': '飲み物取って', 'start': 39.1, 'end': 40.8},
    {'id': 'L05', 'speaker': 'protagonist', 'text': '布団から誘うな！！', 'start': 41.4, 'end': 43.5},
]


def request(url, method='GET', json_data=None, timeout=60):
    body = json.dumps(json_data, ensure_ascii=False).encode('utf-8') if json_data is not None else None
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={'Content-Type': 'application/json'} if body is not None else {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise RuntimeError(f'Engine request failed: {method} {url.split("?")[0]} : {exc}') from exc


def resolve_speakers(speakers):
    """Map actual /speakers style IDs, never the AivisHub model-local style IDs."""
    if not isinstance(speakers, list):
        raise ValueError('/speakers must be an array')
    found = {}
    for role, v in VOICES.items():
        matched = [s for s in speakers if s.get('speaker_uuid') == v['speaker_uuid'] and s.get('name') == v['name']]
        if len(matched) != 1:
            raise ValueError(f'{role}: expected exact speaker name+UUID not loaded: {v["name"]} / {v["speaker_uuid"]}')
        styles = [s for s in matched[0].get('styles', []) if s.get('name') == v['style'] and type(s.get('id')) is int]
        if len(styles) != 1:
            raise ValueError(f'{role}: required runtime style {v["style"]} not found uniquely')
        found[role] = {**v, 'runtime_style_id': styles[0]['id']}
    return found


def measure_wav(data, threshold_dbfs=-40.0):
    """10ms peak detector; approximate audible region only, never a listening substitute."""
    with wave.open(io.BytesIO(data), 'rb') as wf:
        channels, rate, width, total, compression = wf.getnchannels(), wf.getframerate(), wf.getsampwidth(), wf.getnframes(), wf.getcomptype()
        if channels not in (1, 2) or width != 2 or compression != 'NONE':
            raise ValueError(f'Unsupported PCM WAV: channels={channels}, samplewidth={width}, comp={compression}')
        raw = wf.readframes(total)
    samples = struct.unpack('<' + 'h' * (len(raw) // 2), raw)
    step = max(1, round(rate * 0.01)) * channels
    amplitude = 32768 * (10 ** (threshold_dbfs / 20))
    active = [i for i in range(0, len(samples), step) if max((abs(x) for x in samples[i:i+step]), default=0) >= amplitude]
    duration = total / rate
    if not active:
        return {'duration_s': round(duration, 3), 'active_s': 0, 'leading_s': None, 'trailing_s': None, 'sample_rate': rate, 'channels': channels, 'qc': 'SILENCE'}
    onset = active[0] / channels / rate
    offset = min(duration, (active[-1] + step) / channels / rate)
    return {'duration_s': round(duration, 3), 'active_s': round(offset-onset, 3), 'leading_s': round(onset, 3), 'trailing_s': round(duration-offset, 3), 'sample_rate': rate, 'channels': channels, 'qc': 'MEASURED_NOT_LISTENED'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--url', default='http://127.0.0.1:10101')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true', help='Explicitly generate all 5 provisional WAV clips')
    args = ap.parse_args()
    parsed = urllib.parse.urlparse(args.url)
    if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1', 'localhost', '::1'):
        ap.error('Only a local HTTP engine address is permitted')
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    base = args.url.rstrip('/')
    speakers = json.loads(request(base + '/speakers'))
    voice_map = resolve_speakers(speakers)
    (out / 'speakers_resolved.json').write_text(json.dumps({'source_sha': SOURCE_SHA, 'source_pr': SOURCE_PR, 'status': 'PROVISIONAL / G3 NOT APPROVED', 'voices': voice_map}, ensure_ascii=False, indent=2), encoding='utf-8')
    for role, v in voice_map.items():
        print(f'{role}: {v["name"]} / {v["style"]} runtime_style_id={v["runtime_style_id"]}')
    if not args.render:
        print('Discovery finished. For private provisional synthesis, append --render.')
        return
    rows = []
    for line in LINES:
        v = voice_map[line['speaker']]
        params = urllib.parse.urlencode({'text': line['text'], 'speaker': v['runtime_style_id']})
        query = json.loads(request(f'{base}/audio_query?{params}', method='POST'))
        if query.get('speedScale') != 1.0:
            print(f'WARNING: {line["id"]} audio_query speedScale={query.get("speedScale")}; no speed alteration applied', file=sys.stderr)
        wav = request(f'{base}/synthesis?' + urllib.parse.urlencode({'speaker': v['runtime_style_id']}), method='POST', json_data=query)
        filename = f'PR29_A_{line["id"]}_{line["speaker"]}.wav'
        (out / filename).write_bytes(wav)
        m = measure_wav(wav)
        slot = round(line['end'] - line['start'], 3)
        status = 'RETIME_REQUIRED' if m['active_s'] > slot else 'LISTEN_AND_CONFIRM'
        row = {'script_source': 'PR29_A', 'source_sha': SOURCE_SHA, 'line_id': line['id'], 'speaker_id': line['speaker'], 'model_uuid': v['model_uuid'], 'speaker_uuid': v['speaker_uuid'], 'style_name': v['style'], 'runtime_style_id': v['runtime_style_id'], 'text': line['text'], 'slot_start_s': line['start'], 'slot_end_s': line['end'], 'slot_s': slot, 'file': filename, **m, 'status': status, 'rights': 'M2_G3_HOLD' if line['speaker'] == 'organizer' else 'G3_NOT_APPROVED'}
        rows.append(row)
        print(f'{line["id"]}: {line["text"]} active={m["active_s"]:.3f}s slot={slot:.3f}s [{status}]')
    with (out / 'provisional_audio_manifest.csv').open('w', encoding='utf-8-sig', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (out / 'measurement.json').write_text(json.dumps({'source_sha': SOURCE_SHA, 'do_not_publish': True, 'unreviewed_listening': True, 'rights_status': 'M2 unresolved for G3', 'lines': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'WAVs/measurements in {out}. Human listening, text reading and rights review still required; NEVER publish or merge these as approved audio.')


if __name__ == '__main__':
    main()
