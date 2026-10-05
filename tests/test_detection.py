from analyzer.anomaly_detector import AnomalyDetector


def test_traffic_spike_detection():

    detector = AnomalyDetector(
        traffic_spike_threshold=5,
        detection_window=10
    )

    timestamp = 1000

    for _ in range(6):
        detector.record_packet(
            src_ip="192.168.1.10",
            dst_ip="192.168.1.20",
            dst_port="-",
            timestamp=timestamp
        )

    alerts = detector.analyze()

    assert any(
        alert["type"] == "TRAFFIC_SPIKE"
        for alert in alerts
    )


def test_port_scan_detection():

    detector = AnomalyDetector(
        port_scan_threshold=5,
        detection_window=10
    )

    timestamp = 1000

    for port in range(20, 25):

        detector.record_packet(
            src_ip="192.168.1.50",
            dst_ip="192.168.1.20",
            dst_port=port,
            is_tcp_syn=True,
            timestamp=timestamp
        )

    alerts = detector.analyze()

    assert any(
        alert["type"] == "PORT_SCAN"
        for alert in alerts
    )


def test_normal_traffic_no_alert():

    detector = AnomalyDetector(
        traffic_spike_threshold=50,
        port_scan_threshold=10,
        detection_window=10
    )

    detector.record_packet(
        src_ip="192.168.1.10",
        dst_ip="192.168.1.20",
        dst_port=443,
        is_tcp_syn=False,
        timestamp=1000
    )

    alerts = detector.analyze()

    assert alerts == []
