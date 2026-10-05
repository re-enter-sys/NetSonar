#!/usr/bin/env python3

import math
import wave
import struct
import os


SAMPLE_RATE = 44100


def generate_tone(
    frequency=440,
    duration=0.2,
    volume=0.3,
    output_file="/tmp/netsonar_tone.wav"
):
    """
    Generate a simple sine-wave audio tone.
    """

    num_samples = int(SAMPLE_RATE * duration)

    with wave.open(output_file, "w") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        for i in range(num_samples):

            sample = (
                volume
                * math.sin(
                    2 * math.pi * frequency * i / SAMPLE_RATE
                )
            )

            value = int(sample * 32767)

            wav.writeframes(
                struct.pack("<h", value)
            )

    return output_file


if __name__ == "__main__":

    print("Generating NetSonar test tone...")

    filename = generate_tone(
        frequency=440,
        duration=1.0,
        volume=0.3
    )

    print(f"Tone generated: {filename}")
    print(f"File exists: {os.path.exists(filename)}")
