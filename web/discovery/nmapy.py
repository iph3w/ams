# https://resources.infosecinstitute.com/topic/port-scanning-using-scapy/
# https://null-byte.wonderhowto.com/how-to/build-stealth-port-scanner-with-scapy-and-python-0164779/
# https://nmap.org/book/firewall-subversion.html
# https://towardsdatascience.com/graph-visualisation-basics-with-python-part-iii-directed-graphs-with-graphviz-50116fb0d670
import dataclasses
import inspect
import logging
from enum import Enum, unique
from warnings import filterwarnings
from scapy.all import traceroute, RandShort, sr, sr1, IP, TCP, ICMP, get_if_addr, conf
from discovery.domain import NetworkNode
from discovery.models import Discovery, Scanner

filterwarnings("ignore")

SYN_ACK = 0x12
RST_ACK = 0x14


@unique
class PortStatus(Enum):
    OPENED = 1
    CLOSED = 2
    FILTERED = 3


class NetworkMapper:
    __pk: int
    __source_port = RandShort()
    __scanner_ip: str = get_if_addr(conf.iface)
    __verbose: bool = False
    __model: Discovery | Scanner = None
    __ports: list
    __target: str
    __node: NetworkNode

    def __init__(self, pk: int, model, target: str, ports: list, all_ip_address: int):
        self.__pk = pk
        self.__model = model
        self.__ports = ports
        self.__all_ip_address = all_ip_address
        self.__target = target
        self.__node = NetworkNode()

    def ping(self):
        try:
            result = sr1(IP(dst=self.__target) / ICMP(), timeout=10)
            if str(type(result)) == "<type 'NoneType'>" or result is None:
                return None
            return True
        except Exception as ex:
            logging.warning(
                "%s > %s > %s", __file__, self.__class__.__name__, inspect.stack()[0][3], extra=ex.__traceback__
            )
            return False

    def traceroute(self) -> list:
        try:
            conf.checkIPsrc = 0
            ans, _ = traceroute(self.__target, dport=443, verbose=self.__verbose)
            return list(dict.fromkeys(
                [self.__scanner_ip] + [x[0] for x in list(list(ans.get_trace().values())[0].values())] + [self.__target]))
        except Exception as ex:
            logging.warning(
                "%s > %s > %s", __file__, self.__class__.__name__, inspect.stack()[0][3], extra=ex.__traceback__
            )

    def __send_tcp_flag__(self, port: int, flags: str):
        result = sr1(
            IP(dst=self.__target) / TCP(sport=self.__source_port, dport=port, flags=flags),
            timeout=10, verbose=self.__verbose
        )
        if str(type(result)) == "<type 'NoneType'>" or result is None:
            return None
        return result

    def __send_tcp_reset__(self, port: int):
        return sr(
            IP(dst=self.__target) / TCP(sport=self.__source_port, dport=port, flags="R"),
            timeout=10, verbose=self.__verbose
        )

    def firewall_detection(self, port: int):
        result = sr1(
            IP(dst=self.__target) / TCP(
                sport=self.__source_port, dport=port, flags="S", options=[('Timestamp', (0, 0))]
            ), timeout=10, verbose=self.__verbose
        )
        if str(type(result)) == "<type 'NoneType'>" or result is None:
            return True
        return False

    def __is_icmp_error__(self, packet) -> bool:
        if packet.haslayer(ICMP):
            if int(packet.getlayer(ICMP).type) == 3 and int(packet.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                return True
        return False

    def tcp_stealth_scan(self, port: int) -> PortStatus:
        port_status: PortStatus = PortStatus.CLOSED
        scan_resp = self.__send_tcp_flag__(port, "S")
        if scan_resp is None:
            port_status = PortStatus.FILTERED
        elif scan_resp.haslayer(TCP):
            if scan_resp.getlayer(TCP).flags == SYN_ACK:
                self.__send_tcp_reset__(port)
                port_status = PortStatus.OPENED
            elif scan_resp.getlayer(TCP).flags == RST_ACK:
                port_status = PortStatus.CLOSED
        elif self.__is_icmp_error__(scan_resp) is True:
            port_status = PortStatus.FILTERED
        return port_status

    def tcp_port_scan(self, port) -> tuple:
        firewall_detected: bool = False
        port_status: PortStatus = PortStatus.FILTERED
        scan_resp = self.__send_tcp_flag__(port, "A")
        if scan_resp is not None and scan_resp.haslayer(TCP):
            if scan_resp.getlayer(TCP).flags == 0x4:
                if scan_resp.getlayer(TCP).window == 0:
                    port_status = PortStatus.CLOSED
                elif scan_resp.getlayer(TCP).window > 0:
                    port_status = PortStatus.OPENED
        elif scan_resp is not None and self.__is_icmp_error__(scan_resp) is True:
            firewall_detected = True
        return firewall_detected, port_status

    def __remove_node__(self):
        self.__model.remove_node(pk=self.__pk, _model=self.__model, name=self.__target)

    def __add_node__(self, name: str, node: dict):
        self.__model.add_node(pk=self.__pk, _model=self.__model, name=name, node=node)

    def __add_edge__(self, node1: str, node2: str):
        self.__model.add_edge(pk=self.__pk, _model=self.__model, node1=node1, node2=node2)

    def __progress__(self, name: str):
        self.__model.set_progress(pk=self.__pk, _model=self.__model, name=name)

    def start(self):
        if self.ping() in (False, None):
            self.__remove_node__()
            return False
        for idx, port in enumerate(self.__ports):
            self.__node.port = port
            status = self.tcp_stealth_scan(port)
            if status in (PortStatus.CLOSED, PortStatus.FILTERED) and self.__node.firewall_detected is False:
                self.__node.firewall_detected, status = self.tcp_port_scan(port)
                if self.__node.firewall_detected is False:
                    self.__node.firewall_detected = self.firewall_detection(port)
            if status == PortStatus.OPENED:
                self.__node.opened_ports.append(port)
                self.__add_node__(node=dataclasses.asdict(self.__node), name=self.__target)
            elif status == PortStatus.FILTERED:
                pass
                # node.filtered_ports.append(port)
            elif status == PortStatus.CLOSED:
                pass
                # node.closed_ports.append(port)
            self.__node.progress = ((idx + 1) / len(self.__ports)) * 100
        if len(self.__node.opened_ports) > 0:
            last_hop = ""
            for hop in self.traceroute():
                self.__add_node__(node={}, name=hop)
                if last_hop != "":
                    self.__add_edge__(node1=last_hop, node2=hop)
                last_hop = hop
        self.__progress__(name=self.__target)
        return True
