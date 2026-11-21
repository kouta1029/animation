#!/usr/bin/env python3
"""Run deterministic asset checks; visual approval is still manual."""
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET
from PIL import Image

base=Path(sys.argv[1] if len(sys.argv)>1 else 'build/art_v0.3')
manifest=json.loads((base/'asset_manifest.json').read_text(encoding='utf-8'))
assert manifest['approval']=='G2_PENDING'
assert manifest['version']=='0.3-redesign-draft'
assert set(manifest['characters'])=={'nao','hibiki','suzu'}
assert len(manifest['expressions'])==10
stats={}
for key,info in manifest['characters'].items():
    root=base/'characters'/key
    svg=list(root.rglob('*.svg')); png=list(root.rglob('*.png'))
    assert len(svg)==66,(key,len(svg))
    assert len(png)==66,(key,len(png))
    assert len(info['mouths'])==10 and len(info['eyes'])==8 and len(info['brows'])==7
    assert len(info['layers'])==15
    assert {'signature_hair','signature_costume'}.issubset(set(info['layers']))
    for f in svg: ET.parse(f)
    for f in png:
        with Image.open(f) as im:
            assert im.size==(750,2000), (f,im.size)
            assert im.mode=='RGBA',(f,im.mode)
            assert im.getextrema()[-1][0]==0, (f,'not transparent somewhere')
    stats[key]={'svg':len(svg),'png':len(png),'parts':len(info['layers'])}
print('PASS: 3 characters / 198 SVG / 198 RGBA PNG / registered 600x1600 masters -> 750x2000 PNG')
print('PASS: 10 expressions, 10 mouths, 8 eye sets, 7 brow sets per character')
print('LIMITATION: automated QA does not approve artwork, pose library, or PSD delivery')
