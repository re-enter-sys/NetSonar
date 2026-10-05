from analyzer.traffic_analyzer import TrafficAnalyzer


def test_packet_count():

    analyzer = TrafficAnalyzer()

    analyzer.analyze_packet(
        "TCP",
        "192.168.1.10",
        "192.168.1.20",
        50000,
        443,
        100
    )

    assert analyzer.total_packets == 1


def test_byte_count():

    analyzer = TrafficAnalyzer()

    analyzer.analyze_packet(
        "TCP",
        "192.168.1.10",
        "192.168.1.20",
        50000,
        443,
        500
    )

    assert analyzer.total_bytes == 500


def test_protocol_tracking():

    analyzer = TrafficAnalyzer()

    analyzer.analyze_packet(
        "HTTPS",
        "192.168.1.10",
        "192.168.1.20",
        50000,
        443,
        100
    )

    stats = analyzer.get_statistics()

    assert stats["protocols"]["HTTPS"] == 1
