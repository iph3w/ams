def popular_tcp_ports():
    # Most commonly open TCP ports
    return [
        80,  # HTTP
        23,  # Telnet
        443,  # HTTPS
        21,  # FTP
        22,  # SSH
        25,  # SMTP
        3389,  # RDP
        110,  # POP3
        445,  # SMB
        139,  # NetBIOS-SSN
        143,  # IMAP
        53,  # DNS
        135,  # MSRPC
        3306,  # MySQL
        8080,  # HTTP-Proxy
        1723,  # PPTP
        111,  # RPCBind
        995,  # POP3S
        993,  # IMAPS
        5900,  # VNC
        5432,  # Postgresql
        1433,  # MSSQL
        4022,  # MSSQL
        135,  # MSSQL
        1434,  # MSQL
    ]


def popular_udp_ports():
    # Most commonly open UDP ports
    return [
        631,  # IRP
        161,  # SNMP
        137,  # NetBIOS-SSN
        123,  # NTP
        138,  # NETBIOS-DGM
        445,  # Miscrosoft-DS
        135,  # MSRPC
        67,  # DHCP
        53,  # DNS
        139,  # NetBIOS-SSN
        500,  # ISAKMP
        68,  # DHCPC
        520,  # RIP
        1900,  # UPNP
        4500,  # nat-t-ike
        514,  # SYSLOG
        49152,  # Varies
        162,  # SNMPTrap
        69,  # TFTP
        1434,  # MSQL
    ]
