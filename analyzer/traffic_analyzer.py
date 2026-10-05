#!/usr/bin/env python3

from collections import Counter
from datetime import datetime
from analyzer.stats_exporter import StatsExporter


class TrafficAnalyzer:

    def __init__(self):
        self.total_packets = 0
        self.total_bytes = 0

        self.protocols = Counter()
        self.source_ips = Counter()
        self.destination_ips = Counter()
        self.destination_ports = Counter()

        self.start_time = datetime.now()
        self.stats_exporter = StatsExporter()

    def analyze_packet(
        self,
        protocol,
        src_ip,
        dst_ip,
        src_port,
        dst_port,
        packet_size
    ):
        """Process packet information."""

        self.total_packets += 1
        self.total_bytes += packet_size

        self.protocols[protocol] += 1
        self.source_ips[src_ip] += 1
        self.destination_ips[dst_ip] += 1
        

        if dst_port != "-":
            self.destination_ports[dst_port] += 1
            
        self.stats_exporter.export(
            self.get_statistics()
        )

    def get_statistics(self):
        """Return current traffic statistics."""

        elapsed = (
            datetime.now() - self.start_time
        ).total_seconds()

        packets_per_second = (
            self.total_packets / elapsed
            if elapsed > 0
            else 0
        )

        return {
            "total_packets": self.total_packets,
            "total_bytes": self.total_bytes,
            "packets_per_second": round(
                packets_per_second,
                2
            ),
            "protocols": dict(self.protocols),
            "unique_source_ips": len(self.source_ips),
            "unique_destination_ips": len(
                self.destination_ips
            ),
            "destination_ports": self.destination_ports
        }

    def display_statistics(self):
        """Display traffic statistics."""

        stats = self.get_statistics()

        print("\n" + "=" * 60)
        print("NETSONAR TRAFFIC ANALYZER")
        print("=" * 60)

        print(
            f"Packets          : "
            f"{stats['total_packets']}"
        )

        print(
            f"Total bytes      : "
            f"{stats['total_bytes']}"
        )

        print(
            f"Packets/sec      : "
            f"{stats['packets_per_second']}"
        )

        print(
            f"Unique sources   : "
            f"{stats['unique_source_ips']}"
        )

        print(
            f"Unique targets   : "
            f"{stats['unique_destination_ips']}"
        )

        print("\nProtocols:")

        for protocol, count in stats[
            "protocols"
        ].items():
            print(
                f"  {protocol:<8}: {count}"
            )

        print("\nDestination ports:")

        for port, count in stats[
            "destination_ports"
        ].most_common(10):
            print(
                f"  {port:<8}: {count}"
            )

        print("=" * 60)


if __name__ == "__main__":

    analyzer = TrafficAnalyzer()

    print("NetSonar Traffic Analyzer test")

    analyzer.analyze_packet(
        "TCP",
        "192.168.124.128",
        "93.184.216.34",
        45000,
        443,
        74
    )

    analyzer.analyze_packet(
        "UDP",
        "192.168.124.128",
        "8.8.8.8",
        50000,
        53,
        80
    )

    analyzer.analyze_packet(
        "ICMP",
        "192.168.124.128",
        "192.168.124.2",
        "-",
        "-",
        98
    )

    analyzer.display_statistics()
