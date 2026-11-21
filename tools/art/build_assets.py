#!/usr/bin/env python3
"""Build ORIGINAL draft 2D cutout character assets (designs are NOT approved).

Requirements: Python 3.10+, pip install cairosvg pillow
Usage: python tools/art/build_assets.py [--output DIRECTORY]
Each layer is an independently exported, registered, transparent PNG.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

W, H = 600, 1600
S = '{http://www.w3.org/2000/svg}'

CAST = {
 'nao': dict(name='宮瀬ナオ', hair='#38445B', skin='#F6D9C7', jacket='#C9B9A0', shirt='#F7F3E9', pants='#3C4355', accent='#52788C', shoes='#EFF1F4', hair_style='short', face='oval'),
 'hibiki': dict(name='天野ヒビキ', hair='#C97843', skin='#F6CEAF', jacket='#3A929B', shirt='#EBA958', pants='#344D63', accent='#F7CB55', shoes='#F8E9D7', hair_style='spiky', face='round'),
 'suzu': dict(name='久住スズ', hair='#534358', skin='#EED3C7', jacket='#9E899E', shirt='#F7F0E8', pants='#4E414B', accent='#9F6578', shoes='#E5D6D7', hair_style='long', face='oval'),
}

# Values in the same 600x1600 canvas are not arbitrary local offsets.
# Render all layer images with unchanged canvas; this prevents drift when compositing.
def make_svg(key, c):
    hair, skin, coat, shirt, pants, accent, shoes = [c[x] for x in ('hair','skin','jacket','shirt','pants','accent','shoes')]
    round_face = c['face'] == 'round'
    hw = 174 if round_face else 157
    face = f'<path d="M {300-hw} 290 Q {300-hw-8} 139 300 155 Q {300+hw+8} 145 {300+hw} 290 Q {300+hw-8} 501 300 510 Q {300-hw+8} 500 {300-hw} 290 Z" fill="{skin}" stroke="#30313B" stroke-width="12"/>'
    back_hair = (f'<path d="M132 278 Q104 106 295 112 Q500 115 482 323 L488 650 Q444 677 424 627 L414 463 Q298 515 186 467 L177 630 Q151 673 119 640 Z" fill="{hair}" stroke="#30313B" stroke-width="12"/>' if key=='suzu' else '')
    if key == 'nao':
        front = f'<path d="M140 272 Q115 166 192 151 L175 115 L250 148 L285 105 L317 147 Q397 105 443 182 L456 287 L412 249 L393 224 L341 231 L305 204 L262 247 L225 225 L174 278 Z" fill="{hair}" stroke="#30313B" stroke-width="11" stroke-linejoin="round"/>'
    elif key == 'hibiki':
        front = f'<path d="M122 261 L136 184 L107 159 L170 160 L179 99 L224 135 L263 97 L295 144 L356 92 L374 154 L427 140 L431 186 L487 207 L455 249 L428 239 L402 215 L346 234 L304 211 L257 254 L224 230 L180 265 Z" fill="{hair}" stroke="#30313B" stroke-width="11" stroke-linejoin="round"/>'
    else:
        front = f'<path d="M135 299 Q128 142 259 132 Q430 103 456 271 L453 465 L420 450 L411 272 Q359 240 335 193 Q280 255 173 261 L177 460 L144 470 Z" fill="{hair}" stroke="#30313B" stroke-width="11"/>'
    skirt = (f'<path d="M219 1220 L273 1220 L280 1470 L212 1470 Z" fill="#6D606D" stroke="#30313B" stroke-width="9"/><path d="M326 1220 L384 1220 L387 1470 L322 1470 Z" fill="#6D606D" stroke="#30313B" stroke-width="9"/><path d="M179 861 Q300 887 422 861 L461 1256 Q300 1314 139 1256 Z" fill="{pants}" stroke="#30313B" stroke-width="11"/>') if key=='suzu' else ''
    trousers = '' if key=='suzu' else f'<path d="M190 1048 L284 1048 L288 1460 L198 1460 Z" fill="{pants}" stroke="#30313B" stroke-width="12"/><path d="M316 1048 L412 1048 L406 1460 L312 1460 Z" fill="{pants}" stroke="#30313B" stroke-width="12"/>'
    # Rigid pieces; final performance adjustments are done through pivots (see manifest).
    groups = [
        ('hair_back',back_hair),
        ('legs',trousers + skirt + f'<path d="M176 1460 Q220 1427 290 1460 L294 1496 L179 1500 Z" fill="{shoes}" stroke="#30313B" stroke-width="11"/><path d="M314 1460 Q362 1430 424 1460 L430 1500 L312 1497 Z" fill="{shoes}" stroke="#30313B" stroke-width="11"/>'),
        ('torso',f'<path d="M226 550 L370 550 Q421 558 449 657 L427 1080 Q304 1121 175 1080 L152 654 Q171 563 226 550 Z" fill="{coat}" stroke="#30313B" stroke-width="12"/><path d="M244 570 L357 570 L353 1033 L250 1033 Z" fill="{shirt}"/><path d="M244 584 L289 735 L274 1015 M357 584 L312 735 L326 1015" stroke="#685C62" stroke-width="8" fill="none"/><circle cx="299" cy="831" r="8" fill="{accent}"/><circle cx="299" cy="927" r="8" fill="{accent}"/>'),
        ('arm_l',f'<path d="M192 591 Q154 596 136 660 L111 942 Q109 977 146 984 L175 962 L207 720 Z" fill="{coat}" stroke="#30313B" stroke-width="12"/><ellipse cx="141" cy="988" rx="35" ry="41" fill="{skin}" stroke="#30313B" stroke-width="10"/>'),
        ('arm_r',f'<path d="M407 588 Q454 587 467 663 L493 943 Q490 984 451 988 L429 961 L395 720 Z" fill="{coat}" stroke="#30313B" stroke-width="12"/><ellipse cx="458" cy="989" rx="35" ry="41" fill="{skin}" stroke="#30313B" stroke-width="10"/>'),
        ('neck',f'<rect x="271" y="490" width="58" height="104" rx="22" fill="{skin}" stroke="#30313B" stroke-width="10"/>'),
        ('head',face + f'<path d="M{300-hw} 324 Q{300-hw-30} 295 {300-hw-13} 350 M{300+hw} 324 Q{300+hw+30} 295 {300+hw+13} 350" fill="none" stroke="#B98782" stroke-width="8"/>'),
        ('hair_front',front),
        ('eye_l','<ellipse cx="242" cy="323" rx="21" ry="32" fill="#30313B"/><circle cx="247" cy="315" r="8" fill="#FFFFFF"/>'),
        ('eye_r','<ellipse cx="358" cy="323" rx="21" ry="32" fill="#30313B"/><circle cx="363" cy="315" r="8" fill="#FFFFFF"/>'),
        ('brow_l','<path d="M211 270 Q238 255 267 271" fill="none" stroke="#30313B" stroke-width="12" stroke-linecap="round"/>'),
        ('brow_r','<path d="M334 271 Q362 255 390 269" fill="none" stroke="#30313B" stroke-width="12" stroke-linecap="round"/>'),
        ('mouth','<path d="M275 409 Q300 425 325 409" fill="none" stroke="#8C4950" stroke-width="9" stroke-linecap="round"/>'),
    ]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{c["name"]} draft cutout master"><title>{c["name"]} - v0.2 unapproved</title>' + ''.join(f'<g id="{ident}">{s}</g>' for ident,s in groups) + '</svg>'

# Mouth shapes: ten distinct expressions, same center, exchangeable during speech.
MOUTHS={
 'neutral':'<path d="M274 410 H326" stroke="#8C4950" stroke-width="9" stroke-linecap="round"/>',
 'smile':'<path d="M271 403 Q300 435 329 403" fill="none" stroke="#8C4950" stroke-width="9" stroke-linecap="round"/>',
 'wide_small':'<ellipse cx="300" cy="408" rx="24" ry="9" fill="#8C4950"/>',
 'wide_mid':'<ellipse cx="300" cy="409" rx="34" ry="15" fill="#8C4950"/>',
 'wide_big':'<ellipse cx="300" cy="408" rx="42" ry="23" fill="#8C4950"/><path d="M265 405 H335" stroke="#FFFFFF" stroke-width="5"/>',
 'vertical_small':'<ellipse cx="300" cy="409" rx="14" ry="20" fill="#8C4950"/>',
 'vertical_big':'<ellipse cx="300" cy="410" rx="22" ry="37" fill="#8C4950"/>',
 'o_small':'<ellipse cx="300" cy="410" rx="12" ry="12" fill="none" stroke="#8C4950" stroke-width="8"/>',
 'o_big':'<ellipse cx="300" cy="410" rx="25" ry="30" fill="none" stroke="#8C4950" stroke-width="8"/>',
 'frown':'<path d="M270 422 Q300 390 330 422" fill="none" stroke="#8C4950" stroke-width="9" stroke-linecap="round"/>',
}
EYES=['open','narrow','half','closed_smile','closed_flat','surprised','sideeye','tearful']
BROWS=['normal','happy','worried','angry','sad','surprised','single_raised']
EXPRESSIONS={
 'normal':('open','normal','neutral'),'smile':('closed_smile','happy','smile'),
 'surprise':('surprised','surprised','o_big'),'angry':('narrow','angry','wide_big'),
 'confused':('sideeye','worried','frown'),'panic':('surprised','worried','vertical_big'),
 'sad':('tearful','sad','frown'),'shy':('narrow','sad','smile'),
 'smug':('half','single_raised','smile'),'blank':('half','normal','neutral')}


def eye_shape(style, x):
    y=323
    if style in ['closed_smile','closed_flat']:
        cy=315 if style=='closed_smile' else 328
        return f'<path d="M{x-26} {cy} Q{x} {cy+(-29 if style=="closed_smile" else 0)} {x+26} {cy}" fill="none" stroke="#30313B" stroke-width="11" stroke-linecap="round"/>'
    rh={'open':30,'narrow':13,'half':17,'surprised':40,'sideeye':20,'tearful':26}[style]
    rx={'surprised':25,'narrow':24}.get(style,21)
    shift=10 if style=='sideeye' else 0
    tear=f'<path d="M{x+30} 358 Q{x+46} 382 {x+31} 393 Q{x+13} 381 {x+30} 358" fill="#7DBAD8"/>' if style=='tearful' else ''
    return f'<ellipse cx="{x+shift}" cy="{y}" rx="{rx}" ry="{rh}" fill="#30313B"/><circle cx="{x+shift+5}" cy="{y-9}" r="7" fill="#FFFFFF"/>'+tear

def brow_shape(style,x,left):
    y=270
    pts={
        'normal':(-4,-9,-4),'happy':(7,-24,7),'worried':(-13,-19,12),
        'angry':(-19,-4,13) if left else (13,-4,-19),
        'sad':(15,-9,-14) if left else (-14,-9,15),
        'surprised':(-25,-37,-25),
        'single_raised':(-25,-39,-25) if left else (-4,-9,-4),
    }[style]
    a,b,c=pts
    return f'<path d="M{x-27} {y+a} Q{x} {y+b} {x+27} {y+c}" fill="none" stroke="#30313B" stroke-width="11" stroke-linecap="round"/>'

def standalone(fragment, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>{label}</title>{fragment}</svg>'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='build/art_v0.2')
    ap.add_argument('--svg-only',action='store_true',help='skip png if CairoSVG unavailable')
    args=ap.parse_args()
    out=Path(args.output)
    if not args.svg_only:
        try: import cairosvg
        except ImportError as e: raise SystemExit('Install export dependency: pip install cairosvg') from e
    manifest={'version':'0.2-draft','approval':'G2_PENDING','source':'character_parts_spec_v0.1','canvas':{'width':W,'height':H},'output_png_height':2000,'render_registration':'all parts retain same viewBox (600x1600)','characters':{},'expressions':EXPRESSIONS}
    for key,c in CAST.items():
        root=out/'characters'/key
        masters=root/'master'; layers=root/'layers'; mouths=root/'mouths'; eyes=root/'eyes'; brows=root/'brows'
        for p in [masters,layers,mouths,eyes,brows]:p.mkdir(parents=True,exist_ok=True)
        svg=make_svg(key,c)
        (masters/f'{key}_cutout_master.svg').write_text(svg,encoding='utf-8')
        tree=ET.fromstring(svg)
        base_ids=[]
        for node in list(tree):
            if node.tag!=S+'g': continue
            k=node.get('id');base_ids.append(k)
            fragment=ET.tostring(node,encoding='unicode')
            # ElementTree prefixes its serialized SVG namespace; still valid svg.
            dest=layers/f'{key}_{k}.svg'
            dest.write_text(standalone(fragment, f'{key} {k}'),encoding='utf-8')
        for state,fragment in MOUTHS.items():
            (mouths/f'{key}_mouth_{state}.svg').write_text(standalone(fragment,f'{key} mouth {state}'),encoding='utf-8')
        for state in EYES:
            for side,x in [('l',242),('r',358)]:
                (eyes/f'{key}_eye_{state}_{side}.svg').write_text(standalone(eye_shape(state,x),f'{key} eye {state} {side}'),encoding='utf-8')
        for state in BROWS:
            for side,x in [('l',242),('r',358)]:
                (brows/f'{key}_brow_{state}_{side}.svg').write_text(standalone(brow_shape(state,x,side=='l'),f'{key} brow {state} {side}'),encoding='utf-8')
        expdir=root/'expressions'
        expdir.mkdir(parents=True,exist_ok=True)
        for emotion,(eye,brow,mouth) in EXPRESSIONS.items():
            svgroot=ET.fromstring(svg)
            for node in list(svgroot):
                if node.tag!=S+'g': continue
                nodeid=node.get('id')
                newfragment=None
                if nodeid=='eye_l': newfragment=eye_shape(eye,242)
                if nodeid=='eye_r': newfragment=eye_shape(eye,358)
                if nodeid=='brow_l': newfragment=brow_shape(brow,242,True)
                if nodeid=='brow_r': newfragment=brow_shape(brow,358,False)
                if nodeid=='mouth': newfragment=MOUTHS[mouth]
                if newfragment is not None:
                    replacement=ET.fromstring(standalone(f'<g id=\"{nodeid}\">'+newfragment+'</g>',nodeid))
                    pos=list(svgroot).index(node)
                    svgroot.remove(node)
                    svgroot.insert(pos,next(a for a in replacement if a.tag==S+'g'))
            (expdir/f'{key}_expression_{emotion}.svg').write_text(ET.tostring(svgroot,encoding='unicode'),encoding='utf-8')
        if not args.svg_only:
            for file in root.rglob('*.svg'):
                png=file.with_suffix('.png')
                cairosvg.svg2png(url=str(file),write_to=str(png),output_height=2000,output_width=750)
        manifest['characters'][key]={'name':c['name'],'colors':{k:v for k,v in c.items() if k not in ('name','hair_style','face')},'layers':base_ids,'master':str(masters.relative_to(out)/f'{key}_cutout_master.svg'),'pivot_points':{'head':[300,520],'torso':[300,610],'arm_l':[194,620],'arm_r':[406,620],'legs':[300,1050]},'mouths':list(MOUTHS),'eyes':EYES,'brows':BROWS}
    (out/'asset_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Built',out,'characters=',len(CAST),'layer files=',sum(1 for _ in out.rglob('*.svg')))
    print('DESIGN STATUS: G2_PENDING; static draft base rigs, not a validated PSD or completed action library')

if __name__=='__main__': main()
