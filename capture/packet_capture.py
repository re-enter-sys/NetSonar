#!/usr/bin/env python3

from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime
import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from analyzer.traffic_analyzer import TrafficAnalyzer
from analyzer.anomaly_detector import AnomalyDetector
from audio.sound_engine import SoundEngine
from analyzer.event_logger import EventLogger
from analyzer.protocol_analyzer import ProtocolAnalyzer

# Network interface
INTERFACE = "eth0"

# Traffic analyzer
analyzer = TrafficAnalyzer()
detector = AnomalyDetector()
sound_engine = SoundEngine()
event_logger = EventLogger()
protocol_analyzer = ProtocolAnalyzer()

def process_packet(packet):
    """Parse a packet and send it to the traffic analyzer."""

    if IP not in packet:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    packet_size = len(packet)

    protocol = "OTHER"
    src_port = "-"
    dst_port = "-"

    # Always initialize this before checking the protocol
    is_tcp_syn = False

    if TCP in packet:
         protocol = "TCP"
         src_port = packet[TCP].sport
         dst_port = packet[TCP].dport

         is_tcp_syn = (
              bool(packet[TCP].flags & 0x02)
              and not bool(packet[TCP].flags & 0x10)
         )

    elif UDP in packet:
         protocol = "UDP"
         src_port = packet[UDP].sport
         dst_port = packet[UDP].dport

    elif ICMP in packet:
        protocol = "ICMP"


    classified_protocol = protocol_analyzer.identify(
         protocol,
         src_port,
         dst_port
   )

    # Send packet to traffic analyzer
    analyzer.analyze_packet(
        classified_protocol,
        src_ip,
        dst_ip,
        src_port,
        dst_port,
        packet_size,
    )
    
    sound_engine.play_protocol(classified_protocol, packet_size)

    # Send packet to anomaly detector
    detector.record_packet(
        src_ip,
        dst_ip,
        dst_port,
        is_tcp_syn=is_tcp_syn
    )

    # Check for security anomalies
    alerts = detector.analyze()

    for alert in alerts:
        print(
            f"\n[!!! SECURITY ALERT !!!] "
            f"{alert['type']} | "
            f"Severity: {alert['severity']} | "
            f"{alert['message']}\n"
        )
        
        sound_engine.play_alert()
        event_logger.log_event(alert)

    # Display packet
    print(
        f"[{timestamp}] "
        f"{classified_protocol:<8} "
        f"{src_ip}:{src_port} -> "
        f"{dst_ip}:{dst_port} "
        f"SIZE={packet_size}"
    )


def start_capture():
    """Start live network capture."""

    print("=" * 70)
    print("NETSONAR - LIVE NETWORK ANALYZER")
    print("=" * 70)
    print(f"Interface : {INTERFACE}")
    print("Status    : CAPTURING")
    print("Press CTRL+C to stop")
    print("=" * 70)

    try:
        sniff(
            iface=INTERFACE,
            prn=process_packet,
            store=False
        )

    except PermissionError:
        print("[!] Permission denied. Run with sudo.")

    finally:
        print("\n\n[+] Capture stopped.")
        analyzer.display_statistics()


if __name__ == "__main__":
    start_capture()
