#!/usr/bin/env python3


class ProtocolAnalyzer:

    TCP_PROTOCOLS = {
        20: "FTP-DATA",
        21: "FTP",
        22: "SSH",
        23: "TELNET",
        25: "SMTP",
        53: "DNS-TCP",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3389: "RDP",
    }

    UDP_PROTOCOLS = {
        53: "DNS",
        67: "DHCP",
        68: "DHCP",
        123: "NTP",
        161: "SNMP",
        500: "IKE",
        1900: "SSDP",
    }

    @classmethod
    def identify(cls, protocol, src_port, dst_port):

        if protocol == "TCP":

            if dst_port in cls.TCP_PROTOCOLS:
                return cls.TCP_PROTOCOLS[dst_port]

            if src_port in cls.TCP_PROTOCOLS:
                return cls.TCP_PROTOCOLS[src_port]

        elif protocol == "UDP":

            if dst_port in cls.UDP_PROTOCOLS:
                return cls.UDP_PROTOCOLS[dst_port]

            if src_port in cls.UDP_PROTOCOLS:
                return cls.UDP_PROTOCOLS[src_port]

        return protocol


if __name__ == "__main__":

    tests = [
        ("TCP", 50000, 443),
        ("UDP", 50000, 53),
        ("TCP", 50000, 22),
        ("TCP", 50000, 80),
        ("ICMP", "-", "-"),
    ]

    print("NETSONAR PROTOCOL ANALYZER")
    print("=" * 40)

    for protocol, src_port, dst_port in tests:

        result = ProtocolAnalyzer.identify(
            protocol,
            src_port,
            dst_port
        )

        print(
            f"{protocol}:{src_port} -> "
            f"{dst_port} = {result}"
        )

