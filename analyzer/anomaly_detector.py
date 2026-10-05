#!/usr/bin/env python3

from collections import defaultdict
from time import time


class AnomalyDetector:

    def __init__(
        self,
        traffic_spike_threshold=50,
        port_scan_threshold=10,
        detection_window=10
    ):
        self.traffic_spike_threshold = traffic_spike_threshold
        self.port_scan_threshold = port_scan_threshold
        self.detection_window = detection_window

        self.packet_timestamps = []

        # Store TCP SYN attempts:
        # {source_ip: [(timestamp, destination_port), ...]}
        self.syn_activity = defaultdict(list)

    def record_packet(
        self,
        src_ip,
        dst_ip,
        dst_port,
        is_tcp_syn=False,
        timestamp=None
    ):
        """
        Record packet activity for anomaly detection.
        """

        if timestamp is None:
            timestamp = time()

        # -----------------------------
        # Traffic-rate tracking
        # -----------------------------

        self.packet_timestamps.append(timestamp)

        cutoff = timestamp - self.detection_window

        self.packet_timestamps = [
            t
            for t in self.packet_timestamps
            if t >= cutoff
        ]

        # -----------------------------
        # TCP SYN tracking
        # -----------------------------

        if is_tcp_syn and dst_port != "-":

            self.syn_activity[src_ip].append(
                (timestamp, dst_port)
            )

        # Remove old SYN activity

        for ip in list(self.syn_activity):

            self.syn_activity[ip] = [
                (t, port)
                for t, port in self.syn_activity[ip]
                if t >= cutoff
            ]

            if not self.syn_activity[ip]:
                del self.syn_activity[ip]

    def detect_traffic_spike(self):
        """
        Detect unusually high packet rate.
        """

        packet_count = len(self.packet_timestamps)

        if packet_count > self.traffic_spike_threshold:

            return {
                "type": "TRAFFIC_SPIKE",
                "severity": "HIGH",
                "packet_count": packet_count,
                "message": (
                    f"High traffic detected: "
                    f"{packet_count} packets "
                    f"in {self.detection_window} seconds"
                )
            }

        return None

    def detect_port_scan(self):
        """
        Detect TCP SYN packets targeting many
        different destination ports.
        """

        for src_ip, activity in self.syn_activity.items():

            unique_ports = {
                port
                for _, port in activity
            }

            if len(unique_ports) >= self.port_scan_threshold:

                return {
                    "type": "PORT_SCAN",
                    "severity": "HIGH",
                    "source_ip": src_ip,
                    "unique_ports": len(unique_ports),
                    "message": (
                        f"Possible TCP SYN port scan "
                        f"detected from {src_ip}: "
                        f"{len(unique_ports)} unique ports"
                    )
                }

        return None

    def analyze(self):
        """
        Run all anomaly detection checks.
        """

        alerts = []

        traffic_alert = self.detect_traffic_spike()

        if traffic_alert:
            alerts.append(traffic_alert)

        port_scan_alert = self.detect_port_scan()

        if port_scan_alert:
            alerts.append(port_scan_alert)

        return alerts


if __name__ == "__main__":

    detector = AnomalyDetector()

    print("=" * 60)
    print("NETSONAR ANOMALY DETECTOR TEST")
    print("=" * 60)

    # Normal traffic
    for _ in range(5):

        detector.record_packet(
            "192.168.124.128",
            "192.168.124.2",
            53,
            is_tcp_syn=False
        )

    print("\nNormal traffic test:")

    alerts = detector.analyze()

    if alerts:

        for alert in alerts:
            print(alert)

    else:

        print("No anomalies detected.")

    # Simulated TCP SYN scan
    print("\nTCP SYN port scan simulation:")

    for port in range(20, 31):

        detector.record_packet(
            "192.168.124.128",
            "192.168.124.2",
            port,
            is_tcp_syn=True
        )

    alerts = detector.analyze()

    for alert in alerts:

        print(
            f"[ALERT] "
            f"{alert['type']} - "
            f"{alert['severity']} - "
            f"{alert['message']}"
        )

    print("=" * 60)
