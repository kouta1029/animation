#!/usr/bin/env bash
set -euo pipefail

source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
output="$(realpath -m -- "${1:?Supply a new output MP4 path}")"
test ! -e "$output"
work="$(mktemp -d)"
trap 'rm -rf -- "$work"' EXIT
export XDG_CACHE_HOME="$work/cache" XDG_DATA_HOME="$work/data" XDG_CONFIG_HOME="$work/config"
mkdir -p "$XDG_CACHE_HOME" "$XDG_DATA_HOME" "$XDG_CONFIG_HOME"

python3 "$source_dir/composition.py" "$work" "${@:2}"
godot --headless --path "$source_dir" --script "$source_dir/render.gd" -- "$work"
ffmpeg -nostdin -hide_banner -loglevel error -xerror \
    -framerate 24 -i "$work/frame%03d.png" -i "$work/opening.wav" \
    -c:v libx264 -threads:v 2 -crf 16 -pix_fmt yuv420p -c:a aac -ar 48000 \
    -movflags +faststart "$work/output.mp4"
ffmpeg -nostdin -hide_banner -loglevel error -xerror -threads 2 \
    -i "$work/output.mp4" -map 0:v -map 0:a -f null -
mv -n -- "$work/output.mp4" "$output"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate \
    -of compact "$output"
