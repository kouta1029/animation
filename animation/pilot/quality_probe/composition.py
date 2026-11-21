"""Draw layered revision artwork and synthesize original room/breath cues."""

import math
import random
import sys
import wave
from array import array
from pathlib import Path

FPS = 24
DURATION = 3
SAMPLE_RATE = 48_000

CAFE = '''
<defs>
  <linearGradient id="wall" x1="0" x2="1" y1="0" y2="1">
    <stop stop-color="#d9b88a"/><stop offset=".54" stop-color="#ac795c"/><stop offset="1" stop-color="#543b36"/>
  </linearGradient>
  <linearGradient id="pane" x1="0" x2="0" y1="0" y2="1">
    <stop stop-color="#f6dc9a"/><stop offset="1" stop-color="#c88d63"/>
  </linearGradient>
  <linearGradient id="coat" x1="0" x2="1" y1="0" y2="1">
    <stop stop-color="#376777"/><stop offset="1" stop-color="#16343f"/>
  </linearGradient>
  <linearGradient id="skin" x1="0" x2="1" y1="0" y2="1">
    <stop stop-color="#ffcf9a"/><stop offset=".7" stop-color="#df9776"/><stop offset="1" stop-color="#b86963"/>
  </linearGradient>
  <linearGradient id="hair" x1="0" x2="1" y1="0" y2="1">
    <stop stop-color="#353741"/><stop offset="1" stop-color="#172d38"/>
  </linearGradient>
  <radialGradient id="glass">
    <stop offset=".10" stop-color="#e2fff0" stop-opacity=".23"/>
    <stop offset=".72" stop-color="#9cdbcd" stop-opacity=".23"/>
    <stop offset="1" stop-color="#5e9b99" stop-opacity=".6"/>
  </radialGradient>
</defs>
<path d="M0 0h1080v1920H0z" fill="url(#wall)"/>
<path d="M-60 333Q155 199 401 344v868H-60z" fill="#92674d"/>
<path d="M-52 355Q150 231 379 354v865H-52z" fill="#674d41"/>
<path d="M-27 380Q155 271 355 380v830H-27z" fill="url(#pane)"/>
<path d="M-26 1080Q33 978 89 1060t84-74q43-75 69 22t124 72v113H-26z" fill="#8a7052" opacity=".42"/>
<path d="M107 340v866M244 334v872M-22 636h379M-22 867h379" stroke="#775640" stroke-width="19" opacity=".65"/>
<path d="M-14 394Q112 310 235 350l-178 841h-71zM245 357l48 17-166 820H78z" fill="#fff1bc" opacity=".20"/>
<path d="M932 375v877M1011 360v903" stroke="#65433a" stroke-width="11" opacity=".34"/>
<path d="M765 0h26v364h-26z" fill="#784d3b" opacity=".83"/>
<path d="M700 407q14-81 79-81t88 81z" fill="#5f453e"/>
<path d="M708 407q73-13 153 0l-9 22H718z" fill="#e6b881"/>
<path d="M720 414h134" stroke="#f8d498" stroke-width="9" stroke-linecap="round"/>
<path d="M0 1289l353-57 227 101 500-73v660H0z" fill="#785244"/>
<path d="M0 1306l357-66 222 100-36 134L0 1507z" fill="#be8c64"/>
<path d="M0 1344l374-75 155 67-49 93L0 1461" fill="none" stroke="#dbaa7b" stroke-width="5" opacity=".56"/>
<path d="M0 1507l543-33 30 446H0z" fill="#67463f"/>
<path d="M0 1531l540-32M0 1698l554-14M116 1524l5 170M382 1510l26 176M224 1694l17 226" stroke="#4d3836" stroke-width="13" opacity=".47"/>
<path d="M22 1481l448-29M18 1494l331-22" stroke="#f9c590" stroke-width="4" opacity=".35"/>
'''

COAT = '''
<path d="M633 1091q-102 55-159 143-61 116-58 303l35 392h629v-656q-102-133-237-182z"
      fill="#16343f" stroke="#162f36" stroke-width="19" stroke-linejoin="round"/>
<path d="M656 1095q-123 29-175 144-67 142-16 372l67 309h548v-652q-100-117-193-153z"
      fill="url(#coat)"/>
<path d="M654 1096l-37 119 96 123 88-147-48-96z" fill="#f0c48b" opacity=".93"/>
<path d="M624 1174l100 119 88-127-18-42-67 105-82-90z" fill="#c99662"/>
<path d="M826 1500l160-31 17 157-155 25z" fill="#254c59" stroke="#5d8084" stroke-width="5"/>
<path d="M854 1517l111-23M557 1473q35 32 72 42M1026 1387l32 56M720 1749l14 163"
      fill="none" stroke="#91a1a0" stroke-width="6" opacity=".54" stroke-linecap="round"/>
<path d="M770 1328v586" stroke="#153744" stroke-width="12"/>
<path d="M797 1402v482" stroke="#ceb187" stroke-width="4" opacity=".53"/>
<path d="M966 1407l33-55 28 66z" fill="#dda467"/>
<path d="M990 1372l-14 29 34 3z" fill="none" stroke="#593f36" stroke-width="3"/>
<path d="M655 1066l103-73 45 173-58 62-81-52z" fill="url(#skin)" stroke="#4c3a39" stroke-width="12"/>
<path d="M661 1100l48 79 47 7" fill="none" stroke="#b77461" stroke-width="8" opacity=".63"/>
'''

HEAD = '''
<path d="M511 665q-48 99-37 175-54 31-43 58 7 19 38 31-12 84 54 134 62 46 151 54 133 8 223-69 71-64 84-161 13-108-44-183-72-94-187-115-131-27-239 76z"
      fill="url(#skin)" stroke="#493a3b" stroke-width="15" stroke-linejoin="round"/>
<path d="M943 862q47-41 70 3 21 62-42 104-30 15-55-10" fill="#e8a080" stroke="#593e3b" stroke-width="12"/>
<path d="M963 921q11-31 31-32" fill="none" stroke="#a56057" stroke-width="8" stroke-linecap="round"/>
<path d="M486 753q-82-153 11-246T753 417q62-25 99-99 32 57 10 113 87 10 123 64 50 75 37 190-8 85-70 182l-36-15-38-108q-58-44-101-122-27 115-159 170 27-57 26-103-36 90-167 140z"
      fill="url(#hair)" stroke="#21313b" stroke-width="17" stroke-linejoin="round"/>
<path d="M489 642q-28-108 101-157 84-34 166-17M638 587q106-36 169-115M877 485q87 82 100 224M538 699q36-19 78-65"
      fill="none" stroke="#6d6e6b" stroke-width="12" opacity=".50" stroke-linecap="round"/>
<path d="M835 680l69 32M824 706l67 32" stroke="#f4be76" stroke-width="11" stroke-linecap="round"/>
<path d="M835 679l26 12M825 705l26 12" stroke="#ffdd9b" stroke-width="4" stroke-linecap="round"/>
<path d="M674 964q61-25 103-8" fill="none" stroke="#f3b391" stroke-width="18" opacity=".45" stroke-linecap="round"/>
<path d="M440 891q28 13 46 2" fill="none" stroke="#ac685b" stroke-width="6" stroke-linecap="round"/>
'''

FOREARM = '''
<path d="M723 1350q-95-139-194-102-117 54-188 152l70 68q109-9 229-47z"
      fill="url(#coat)" stroke="#243b45" stroke-width="15" stroke-linejoin="round"/>
<path d="M397 1362q-46 18-70 56-35 14-56 32-24 27 7 41 16 6 51-4 36 12 73-15l44-63z"
      fill="url(#skin)" stroke="#563e3b" stroke-width="11" stroke-linejoin="round"/>
<path d="M364 1382l56 74 31-16-53-76z" fill="#bb956d"/>
<path d="M341 1452q-20 10-37 18" fill="none" stroke="#a26758" stroke-width="5" stroke-linecap="round"/>
<path d="M480 1362q58-44 119-36" fill="none" stroke="#709292" stroke-width="7" opacity=".72" stroke-linecap="round"/>
'''


def smooth(start, stop, value):
    fraction = min(1.0, max(0.0, (value - start) / (stop - start)))
    return fraction * fraction * (3.0 - 2.0 * fraction)


def make_frame(index):
    settle = smooth(0, 17, index)
    recover = smooth(49, 68, index)
    look = smooth(39, 54, index)
    surprise = smooth(47, 58, index)
    breath = smooth(16, 22, index) * (1 - smooth(39, 53, index))
    shoulder = 56 * settle - 17 * recover
    head_drop = 31 * settle - 13 * recover
    head_turn = 4.0 * settle - 7.5 * recover
    eye_open = 19 + 17 * surprise - 6.0 * settle
    pupil_x = 576 - 12 * look
    pupil_y = 835 - 15 * look
    breath_mouth_y = 3 + 15 * breath
    lower_arm = 55 * (1 - smooth(0, 12, index)) + 4 * math.sin(index * 0.16) * (1 - settle)
    mouth_x = 467
    mouth_y = 971

    # The bubble begins at the lip and then moves away, leaving the gaze readable.
    birth = smooth(18, 35, index)
    rise = smooth(34, 71, index)
    balloon = ""
    if index >= 18:
        radius = 4 + 70 * birth
        tilt = math.radians(head_turn)
        lip_x = 740 + (mouth_x - 740) * math.cos(tilt) - (mouth_y - 1100) * math.sin(tilt)
        lip_y = 1100 + (mouth_x - 740) * math.sin(tilt) + (mouth_y - 1100) * math.cos(tilt)
        bx = lip_x - radius * .95 - 122 * rise + 8 * math.sin(math.pi * rise * 1.4)
        by = lip_y + head_drop - 7 * birth - 350 * rise
        balloon = f"""
<g transform="translate({bx:.2f},{by:.2f}) scale({radius / 68:.3f})">
  <path d="M-7 70q-21 24-12 43" fill="none" stroke="#89a0a1" stroke-width="4" stroke-linecap="round" opacity=".85"/>
  <path d="M0-74c39 0 70 33 70 73q0 49-69 76-66-23-69-73c-2-41 28-76 68-76z"
        fill="url(#glass)" stroke="#537c7d" stroke-width="6"/>
  <path d="M-48-27q12-24 40-28M-52-11l1-4" fill="none" stroke="#fff0c5" stroke-width="10" stroke-linecap="round" opacity=".84"/>
  <path d="M46 24q-11 24-42 35" fill="none" stroke="#cfefe0" stroke-width="5" stroke-linecap="round" opacity=".56"/>
  <path d="M1 73l-11 9 11 5 11-5z" fill="#668f90"/>
</g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
{CAFE}
<g transform="translate(0,{shoulder:.2f})">{COAT}</g>
<g transform="translate(0,{head_drop:.2f}) rotate({head_turn:.2f},740,1100)">
{HEAD}
<path d="M532 {800 - 30 * surprise:.2f}q43-27 99-12" fill="none" stroke="#463d3b" stroke-width="11" stroke-linecap="round"/>
<path d="M542 838q32 {-eye_open * 1.7:.2f} 72 -13q-1 {eye_open * 1.9:.2f}-40 {eye_open * 1.35:.2f}q-23-3-32 {-eye_open * 0.85:.2f}z"
      fill="#fff0db" stroke="#594640" stroke-width="8" stroke-linejoin="round"/>
<ellipse cx="{pupil_x:.2f}" cy="{pupil_y:.2f}" rx="12" ry="{min(17, eye_open + 3):.2f}" fill="#35464b"/>
<circle cx="{pupil_x-4:.2f}" cy="{pupil_y-4:.2f}" r="4" fill="#fff0d4"/>
<ellipse cx="{mouth_x:.2f}" cy="{mouth_y:.2f}" rx="{10+14*breath:.2f}" ry="{breath_mouth_y:.2f}"
         transform="rotate(11,{mouth_x},{mouth_y})" fill="#633d42" stroke="#a35f56" stroke-width="5"/>
</g>
<g transform="translate(0,{-lower_arm:.2f})">{FOREARM}</g>
{balloon}
</svg>"""


def make_audio(path):
    rng = random.Random(24)
    samples = array("h")
    low, breath_body = 0.0, 0.0
    for index in range(SAMPLE_RATE * DURATION):
        seconds = index / SAMPLE_RATE
        noise = rng.uniform(-1, 1)
        low = 0.96 * low + 0.04 * noise
        breath_body = 0.81 * breath_body + 0.19 * noise
        room = low * 0.013
        breath_level = smooth(.70, .87, seconds) * (1 - smooth(1.36, 1.92, seconds))
        breath = (breath_body - low * .85) * breath_level * 0.21
        elbow_time = max(0, seconds - .45)
        elbow = math.sin(math.tau * 87 * elbow_time) * math.exp(-47 * elbow_time) * (1-math.exp(-180*elbow_time)) * .055
        lift_time = max(0, seconds - 1.33)
        lift = math.sin(math.tau * (410 * lift_time + 240 * lift_time**2)) * math.exp(-18 * lift_time) * (1-math.exp(-50*lift_time)) * .031
        taper = smooth(0, .07, seconds) * (1-smooth(2.90, 3.0, seconds))
        samples.append(round(32767 * taper * (room + breath + elbow + lift)))
    if sys.byteorder != "little":
        samples.byteswap()
    with wave.open(str(path), "wb") as sound:
        sound.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
        sound.writeframes(samples.tobytes())


if __name__ == "__main__":
    directory = Path(sys.argv[1])
    for frame_index in range(FPS * DURATION):
        (directory / f"frame{frame_index:03d}.svg").write_text(make_frame(frame_index), encoding="utf-8")
    make_audio(directory / "opening.wav")
