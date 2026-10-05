#!/usr/bin/env python3

import json
import os


class StatsExporter:

    def __init__(self, output_file="data/live_stats.json"):
        self.output_file = output_file

        directory = os.path.dirname(output_file)

        if directory:
            os.makedirs(directory, exist_ok=True)

    def export(self, statistics):

        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                statistics,
                file,
                indent=4
            )
