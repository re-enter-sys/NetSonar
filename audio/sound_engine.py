#!/usr/bin/env python3

import os
import subprocess
import tempfile

from audio.tones import generate_tone
from analyzer.audio_exporter import AudioExporter


class SoundEngine:

    PROTOCOL_FREQUENCIES = {
        "TCP": 440,
        "UDP": 660,
        "ICMP": 880,
        "DNS": 1000,
        "HTTPS": 550,
        "HTTP": 500,
        "SSH": 600,
        "FTP": 620,
        "SMTP": 680,
        "NTP": 760,
        "DHCP": 800,
        "SNMP": 820,
        "RDP": 900,
        "SMB": 940,
        "OTHER": 300,
    }

    def __init__(self):

        self.audio_dir = os.path.join(
            tempfile.gettempdir(),
            "netsonar_audio"
        )

        os.makedirs(
            self.audio_dir,
            exist_ok=True
        )

        self.audio_exporter = AudioExporter()

    def play_tone(
        self,
        frequency,
        duration=0.08,
        volume=0.25
    ):

        frequency = int(
            max(
                100,
                min(frequency, 2000)
            )
        )

        duration = max(
            0.03,
            min(duration, 0.5)
        )

        volume = max(
            0.05,
            min(volume, 0.8)
        )

        filename = os.path.join(
            self.audio_dir,
            f"tone_{frequency}_"
            f"{int(duration * 1000)}_"
            f"{int(volume * 100)}.wav"
        )

        if not os.path.exists(filename):

            generate_tone(
                frequency=frequency,
                duration=duration,
                volume=volume,
                output_file=filename
            )

        subprocess.Popen(
            [
                "aplay",
                "-q",
                filename
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def play_protocol(
        self,
        protocol,
        packet_size=100
    ):

        base_frequency = self.PROTOCOL_FREQUENCIES.get(
            protocol,
            self.PROTOCOL_FREQUENCIES["OTHER"]
        )

        frequency = base_frequency + min(
            packet_size // 20,
            200
        )

        volume = 0.15 + min(
            packet_size / 1500,
            0.45
        )

        duration = 0.05 + min(
            packet_size / 5000,
            0.20
        )

        # Play actual audio
        self.play_tone(
            frequency=frequency,
            duration=duration,
            volume=volume
        )

        # Export audio telemetry for dashboard
        self.audio_exporter.export(
            protocol=protocol,
            frequency=frequency,
            duration=duration,
            volume=volume,
            packet_size=packet_size,
            alert=False
        )

    def play_alert(self):

        alert_tones = [
            (1200, 0.12, 0.5),
            (700, 0.12, 0.5)
        ]

        for frequency, duration, volume in alert_tones:

            # Play alert sound
            self.play_tone(
                frequency=frequency,
                duration=duration,
                volume=volume
            )

            # Export alert telemetry
            self.audio_exporter.export(
                protocol="SECURITY_ALERT",
                frequency=frequency,
                duration=duration,
                volume=volume,
                packet_size=0,
                alert=True
            )


if __name__ == "__main__":

    engine = SoundEngine()

    print(
        "NETSONAR DYNAMIC SOUND ENGINE"
    )

    print("=" * 50)

    print("Testing TCP...")
    engine.play_protocol(
        "TCP",
        60
    )

    print("Testing HTTPS...")
    engine.play_protocol(
        "HTTPS",
        74
    )

    print("Testing DNS...")
    engine.play_protocol(
        "DNS",
        71
    )

    print("Testing ICMP...")
    engine.play_protocol(
        "ICMP",
        98
    )

    print("Testing security alert...")
    engine.play_alert()

    print()
    print("Audio + telemetry test complete.")
