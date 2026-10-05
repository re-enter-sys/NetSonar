#!/usr/bin/env python3

import os
from datetime import datetime


class EventLogger:

    def __init__(self, log_file="logs/network_events.log"):

        self.log_file = log_file

        log_directory = os.path.dirname(
            self.log_file
        )

        if log_directory:
            os.makedirs(
                log_directory,
                exist_ok=True
            )

    def log_event(self, alert):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_entry = (
            f"[{timestamp}] "
            f"TYPE={alert.get('type', 'UNKNOWN')} "
            f"SEVERITY={alert.get('severity', 'UNKNOWN')} "
            f"MESSAGE={alert.get('message', '')}"
        )

        if alert.get("source_ip"):
            log_entry += (
                f" SOURCE_IP={alert['source_ip']}"
            )

        if alert.get("unique_ports"):
            log_entry += (
                f" UNIQUE_PORTS={alert['unique_ports']}"
            )

        if alert.get("packet_count"):
            log_entry += (
                f" PACKETS={alert['packet_count']}"
            )

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as log:

            log.write(
                log_entry + "\n"
            )

        return log_entry


if __name__ == "__main__":

    logger = EventLogger()

    test_alert = {
        "type": "PORT_SCAN",
        "severity": "HIGH",
        "source_ip": "192.168.124.50",
        "unique_ports": 25,
        "message": (
            "Possible TCP SYN port scan detected"
        )
    }

    print("Testing NetSonar Event Logger...")
    print("=" * 50)

    entry = logger.log_event(
        test_alert
    )

    print(entry)

    print("\nLog written to:")
    print(logger.log_file)
