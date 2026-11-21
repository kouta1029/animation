#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repository_dir="$(cd -- "$project_dir/../../.." && pwd)"
if [[ $# != 1 ]]; then
    printf 'Usage: %s /absolute/path/to/output.mp4\n' "$0" >&2
    exit 2
fi
output="$(realpath -m -- "$1")"
if [[ -e "$output" ]]; then
    printf 'Output already exists: %s\n' "$output" >&2
    exit 2
fi
artwork_dir="$repository_dir/assets/pilot/animatic"
temp_dir="$(mktemp -d)"
trap 'rm -rf -- "$temp_dir"' EXIT
mkdir -p "$temp_dir"/{cache,config,data,frames}

export XDG_CACHE_HOME="$temp_dir/cache"
export XDG_CONFIG_HOME="$temp_dir/config"
export XDG_DATA_HOME="$temp_dir/data"
cp "$project_dir/cues.ass" "$temp_dir/cues.ass"
cd -- "$temp_dir"
godot --headless --path "$project_dir" --script "$project_dir/render.gd" -- \
    "$artwork_dir" "$temp_dir/frames"
python3 "$project_dir/temp_audio.py" "$temp_dir/cues.wav"
ffmpeg -nostdin -hide_banner -loglevel error -xerror -filter_threads 1 \
    -framerate 24 -i 'frames/frame%04d.png' -i cues.wav \
    -map 0:v:0 -map 1:a:0 -frames:v 1008 \
    -vf 'scale=1080:1920:flags=lanczos,ass=cues.ass' \
    -c:v libx264 -threads:v 2 -preset fast -crf 19 -pix_fmt yuv420p \
    -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$temp_dir/review.mp4"
ffmpeg -nostdin -hide_banner -loglevel error -xerror -threads 2 \
    -i "$temp_dir/review.mp4" -map 0:v -map 0:a -f null -
mv -n -- "$temp_dir/review.mp4" "$output"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate \
    -of compact "$output"
