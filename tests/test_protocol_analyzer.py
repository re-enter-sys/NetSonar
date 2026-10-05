from analyzer.protocol_analyzer import ProtocolAnalyzer


def test_https_detection():
    result = ProtocolAnalyzer.identify(
        "TCP",
        50000,
        443
    )
    assert result == "HTTPS"


def test_http_detection():
    result = ProtocolAnalyzer.identify(
        "TCP",
        50000,
        80
    )
    assert result == "HTTP"


def test_ssh_detection():
    result = ProtocolAnalyzer.identify(
        "TCP",
        50000,
        22
    )
    assert result == "SSH"


def test_dns_detection():
    result = ProtocolAnalyzer.identify(
        "UDP",
        50000,
        53
    )
    assert result == "DNS"


def test_icmp_detection():
    result = ProtocolAnalyzer.identify(
        "ICMP",
        "-",
        "-"
    )
    assert result == "ICMP"
