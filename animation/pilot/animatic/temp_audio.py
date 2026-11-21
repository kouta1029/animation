"""Create original timing cues from oscillators and deterministic filtered noise."""

import math
import random
import struct
import sys
import wave

SAMPLE_RATE = 48_000
DURATION = 42
BREATHS = [(0.75, 1.50), (13.71, 14.50), (17.50, 18.25), (25.00, 27.25)]
LINES = [
    (4.25, 5.30, 205, 4),
    (6.05, 9.00, 205, 11),
    (13.00, 13.46, 205, 2),
    (30.00, 32.75, 205, 11),
    (38.25, 40.50, 169, 10),
]
BIRTHS = [0.88, 13.70, 17.68, 25.32]


def main(output):
    generator = random.Random(1)
    signal = [0.0] * (SAMPLE_RATE * DURATION)
    for start, end in BREATHS:
        filtered = 0.0
        for index in range(round(start * SAMPLE_RATE), round(end * SAMPLE_RATE)):
            progress = (index / SAMPLE_RATE - start) / (end - start)
            filtered = 0.94 * filtered + 0.06 * generator.uniform(-1, 1)
            signal[index] += 0.5 * math.sin(math.pi * progress) ** 1.5 * filtered
    for start, end, pitch, syllables in LINES:
        for index in range(round(start * SAMPLE_RATE), round(end * SAMPLE_RATE)):
            elapsed = index / SAMPLE_RATE - start
            pulse = elapsed / (end - start) * syllables % 1.0
            frequency = pitch * (1.0 + 0.045 * math.sin(elapsed * 5))
            wavelet = math.sin(math.tau * frequency * elapsed)
            signal[index] += 0.065 * wavelet * math.sin(math.pi * pulse) ** 2
    for birth in BIRTHS:
        for index in range(round(birth * SAMPLE_RATE), round((birth + 0.25) * SAMPLE_RATE)):
            elapsed = index / SAMPLE_RATE - birth
            chirp = math.sin(math.tau * (350 * elapsed + 950 * elapsed**2))
            signal[index] += 0.12 * chirp * math.sin(math.pi * elapsed / 0.25) ** 2
    with wave.open(output, "wb") as audio:
        audio.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
        audio.writeframes(b"".join(struct.pack("<h", round(sample * 32767)) for sample in signal))


if __name__ == "__main__":
    main(sys.argv[1])
