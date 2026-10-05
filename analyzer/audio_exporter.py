#!/usr/bin/env python3

import json
import os
from collections import deque
from datetime import datetime


class AudioExporter:

    def __init__(
        self,
        output_file="data/live_audio.json",
        max_events=100
    ):
        self.output_file = output_file
        self.events = deque(maxlen=max_events)

        directory = os.path.dirname(output_file)

        if directory:
            os.makedirs(directory, exist_ok=True)

        self._write()

    def export(
        self,
        protocol,
        frequency,
        duration,
        volume,
        packet_size,
        alert=False
    ):
        event = {
            "timestamp": datetime.now().strftime(
                "%H:%M:%S.%f"
            )[:-3],
            "protocol": protocol,
            "frequency": round(frequency, 2),
            "duration": round(duration, 3),
            "volume": round(volume, 3),
            "packet_size": packet_size,
            "alert": alert
        }

        self.events.append(event)
        self._write()

    def _write(self):
        data = {
            "events": list(self.events)
        }

        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )


if __name__ == "__main__":

    exporter = AudioExporter()

    exporter.export(
        protocol="HTTPS",
        frequency=553,
        duration=0.064,
        volume=0.19,
        packet_size=74
    )

    exporter.export(
        protocol="DNS",
        frequency=1003,
        duration=0.064,
        volume=0.18,
        packet_size=71
    )

    print("NetSonar Audio Exporter test complete.")
    print("Output:", exporter.output_file)
