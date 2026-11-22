#!/usr/bin/env python3
"""Deterministic structure checks and PNG export for G2 3-view concept roughs.

Approval remains a human art-direction decision; this does not verify actual Godot motion.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path("assets/concepts/v0.3")
CAST = ("nao", "hibiki", "suzu")
NS = "{http://www.w3.org/2000/svg}"
EXPECTED_VIEWS = ("FRONT", "LEFT", "RIGHT")

def check_svg(path: Path, *, width: int, height: int):
    assert path.exists(), f"missing image: {path}"
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.tag == NS + "svg", f"not SVG: {path}"
    assert root.attrib["viewBox"] == f"0 0 {width} {height}", (path, root.attrib.get("viewBox"))
    assert len(list(root.iter(NS + "path"))) >= 25, f"not enough illustration primitives: {path}"
    return path.read_text(encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", type=Path, default=None, help="optional directory for preview PNGs")
    args = ap.parse_args()
    for name in CAST:
        path = ROOT / f"{name}_turnaround.svg"
        raw = check_svg(path, width=1560, height=760)
        assert all(view in raw for view in EXPECTED_VIEWS), f"missing view label: {name}"
        assert "scale(-1 1)" in raw, f"right three-quarter draft not found: {name}"
        assert "G2 PENDING" in raw, f"approval warning missing: {name}"
    comparison = check_svg(ROOT / "compare_128px.svg", width=818, height=778)
    expected_scale = 128 / 600
    scales = [float(x) for x in re.findall(r"scale\((0\.\d+)\)", comparison)]
    assert len(scales) == 9, f"128px scale count is {len(scales)} instead of 9"
    assert all(abs(v - expected_scale) < 1e-8 for v in scales), scales

    if args.render is not None:
        try:
            import cairosvg
        except ImportError as exc:
            raise SystemExit("pip install cairosvg") from exc
        args.render.mkdir(parents=True, exist_ok=True)
        for path in [*(ROOT / f"{name}_turnaround.svg" for name in CAST), ROOT / "compare_128px.svg"]:
            png = args.render / path.with_suffix(".png").name
            cairosvg.svg2png(url=str(path), write_to=str(png))
            assert png.stat().st_size > 5000, f"empty preview: {png}"
            print("PREVIEW:", png)
    print("PASS: 3 character turnaround sheets (front, left/right 3/4) and 9 equally scaled 128px comparisons")
    print("LIMITATION: mirrored right 3/4, no proper articulated rig or motion QA; G2_PENDING")

if __name__ == "__main__":
    main()
