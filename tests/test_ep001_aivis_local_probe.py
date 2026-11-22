"""Unit checks: exact speaker UUID matching and WAV silence timing (no engine needed)."""
import io
import math
import struct
import sys
import unittest
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "video"))
from ep001_aivis_local_probe import resolve_speakers, measure_wav, VOICES


class ProbeTests(unittest.TestCase):
    def fake_speakers(self):
        return [
            dict(name=v["name"], speaker_uuid=v["speaker_uuid"],
                 styles=[{"name": v["style"], "id": 422000 + i}])
            for i, v in enumerate(VOICES.values())
        ]

    def test_style_ids_are_runtime_only(self):
        found = resolve_speakers(self.fake_speakers())
        self.assertEqual(found["organizer"]["runtime_style_id"], 422001)

    def test_fail_closed_on_missing_uuid(self):
        speakers = self.fake_speakers()
        speakers[0]["speaker_uuid"] = "not-the-right-model"
        with self.assertRaises(ValueError):
            resolve_speakers(speakers)

    def test_pcm_duration_and_silence(self):
        rate = 16000
        values = [
            int(12000 * math.sin(2 * math.pi * 440 * i / rate))
            if 3200 <= i < 12800 else 0
            for i in range(rate)
        ]
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(rate)
            wav.writeframes(struct.pack("<" + str(len(values)) + "h", *values))
        result = measure_wav(buf.getvalue())
        self.assertAlmostEqual(result["duration_s"], 1.0, places=2)
        self.assertAlmostEqual(result["active_s"], 0.6, places=2)
        self.assertAlmostEqual(result["leading_s"], 0.2, places=2)
        self.assertAlmostEqual(result["trailing_s"], 0.2, places=2)


if __name__ == "__main__":
    unittest.main()
