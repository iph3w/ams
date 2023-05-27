# https://resources.infosecinstitute.com/topic/port-scanning-using-scapy/
# https://null-byte.wonderhowto.com/how-to/build-stealth-port-scanner-with-scapy-and-python-0164779/
# https://nmap.org/book/firewall-subversion.html
# https://towardsdatascience.com/graph-visualisation-basics-with-python-part-iii-directed-graphs-with-graphviz-50116fb0d670
import threading
import typing
import celery
import copy

from enum import Enum, unique
from warnings import filterwarnings
from scapy.all import traceroute, RandShort, sr, sr1, IP, TCP, ICMP, get_if_addr, conf, UDP
from discovery.domain import NetworkNode
from discovery.models import Discovery

filterwarnings("ignore")


MAX_THREAD_WORKER = 10


@unique
class PortStatus(Enum):
    OPENED = 1
    CLOSED = 2
    FILTERED = 3


class DiscoveryTask(celery.Task):
    __source_port = RandShort()
    __scanner_ip: str = get_if_addr(conf.iface)
    __counter_lock: threading.Lock = threading.Lock()
    __counter: int = 0
    __available_ip_address_lock: threading.Lock = threading.Lock()
    __verbose: bool = False
    __ports: typing.List[int] = []
    __available_ip_address: typing.List[str] = []
    __instance: Discovery = None

    def progress(self) -> float:
        res = 0
        with self.__counter_lock:
            self.__counter += 1
            res = float(self.__counter / (len(self.__available_ip_address) * len(self.__ports))) * 100
        return res

    def traceroute(self, target) -> list:
        conf.checkIPsrc = 0
        ans, _ = traceroute(target, dport=443, verbose=self.__verbose)
        return list(dict.fromkeys([self.__scanner_ip] + [x[0] for x in list(list(ans.get_trace().values())[0].values())] + [target]))

    def discover(self, target: str, ports: list):
        node = NetworkNode()
        print(target, ports)
        for idx, port in enumerate(ports):
            node.port = port
            status = self.tcp_stealth_scan(target, port)
            if status in (PortStatus.CLOSED, PortStatus.FILTERED) and node.firewall_detected is False:
                node.firewall_detected, status = self.tcp_port_scan(target, port)
                if node.firewall_detected is False:
                    node.firewall_detected = self.firewall_detection(target, port)
            if status == PortStatus.OPENED:
                node.opened_ports.append(port)
            elif status == PortStatus.FILTERED:
                pass
                # node.filtered_ports.append(port)
            elif status == PortStatus.CLOSED:
                pass
                # node.closed_ports.append(port)
            node.progress = ((idx + 1) / len(ports)) * 100
            self.__instance.set_progress(self.progress())
            self.__instance.add_node(node=node, name=target)
        if len(node.opened_ports) > 0:
            self.__instance.add_node(node=node, name=target)
            last_hop = ""
            for hop in self.traceroute(target):
                self.__instance.add_node(node=None, name=hop)
                if last_hop != "":
                    self.__instance.add_edge(node1=last_hop, node2=hop)
                last_hop = hop
        else:
            self.__instance.remove_node(name=target)
        print(target, 'Done')
        return True

    def __send_tcp_flag__(self, target: str, port: int, flags: str):
        result = sr1(
            IP(dst=target)/TCP(sport=self.__source_port,dport=port,flags=flags),
            timeout=10, verbose=self.__verbose
        )
        if str(type(result)) == "<type 'NoneType'>" or result is None:
            return None
        return result

    def __send_tcp_reset__(self, target: str, port: int):
        return sr(
            IP(dst=target)/TCP(sport=self.__source_port,dport=port,flags="R"),
            timeout=10, verbose=self.__verbose
        )

    def firewall_detection(self, target: str, port: int):
        result = sr1(
            IP(dst=target)/TCP(sport=self.__source_port,dport=port,flags="S", options=[('Timestamp', (0, 0))]),
            timeout=10, verbose=self.__verbose
        )
        if str(type(result)) == "<type 'NoneType'>" or result is None:
            return True
        return False

    def __is_icmp_error__(self, packet) -> bool:
        if packet.haslayer(ICMP):
            if int(packet.getlayer(ICMP).type) == 3 and int(packet.getlayer(ICMP).code) in [1,2,3,9,10,13]:
                return True
        return False

    def tcp_stealth_scan(self, target: str, port: int) -> PortStatus:
        port_status: PortStatus = PortStatus.CLOSED
        scan_resp = self.__send_tcp_flag__(target, port, "S")
        if scan_resp is None:
            port_status = PortStatus.FILTERED
        elif scan_resp.haslayer(TCP):
            if scan_resp.getlayer(TCP).flags == 0x12:
                self.__send_tcp_reset__(target, port)
                port_status = PortStatus.OPENED
            elif scan_resp.getlayer(TCP).flags == 0x14:
                port_status = PortStatus.CLOSED
        elif self.__is_icmp_error__(scan_resp) is True:
                port_status = PortStatus.FILTERED
        return port_status

    def tcp_port_scan(self, target, port) -> tuple:
        firewall_detected: bool = False
        port_status: PortStatus = PortStatus.FILTERED
        scan_resp = self.__send_tcp_flag__(target, port, "A")
        if scan_resp is not None and scan_resp.haslayer(TCP):
            if scan_resp.getlayer(TCP).flags == 0x4:
                if scan_resp.getlayer(TCP).window == 0:
                    port_status = PortStatus.CLOSED
                elif scan_resp.getlayer(TCP).window > 0:
                    port_status = PortStatus.OPENED
        elif scan_resp is not None and self.__is_icmp_error__(scan_resp) is True:
            firewall_detected = True
        return firewall_detected, port_status

    def get_target(self) -> (str | None):
        target = None
        with self.__available_ip_address_lock:
            if len(self.__available_ip_address) > 0:
                target = self.__available_ip_address.pop(0)
        return target

    def scanner(self):
        while True:
            target = self.get_target()
            if target is None or target == "": break
            self.discover(target=target, ports=self.__ports)

    def main(self, *args, **kwargs):
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        print(kwargs)
        if Discovery.objects.filter(pk=kwargs['instance']).exists():
            self.__instance: Discovery = Discovery.objects.get(pk=kwargs['instance'])
        self.__ports = kwargs['ports']
        self.__available_ip_address: typing.List = kwargs['available_ip_address']

        if self.__scanner_ip not in self.__available_ip_address:
            self.__instance.add_node(None, self.__scanner_ip)
        thread_pool: typing.List[threading.Thread] = []
        for _ in range(MAX_THREAD_WORKER):
            thread = threading.Thread(target=self.scanner)
            thread.start()
            thread_pool.append(thread)
        for thread in thread_pool:
            thread.join()
        # chunks_of_ip_addesses = list(chunks(self.__instance.available_ip_address, MAX_THREAD_WORKER))
        # self.__instance.set_progress(0)
        # completed = 0
        # for chunk in chunks_of_ip_addesses:
        #     with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKER) as executor:
        #         futures = [executor.submit(self.discover, ip) for ip in chunk]
        #         wait(futures)
        #         completed += len(futures)
        #         for future in futures:
        #             if future.exception() != None:
        #                 print(future.exception())
        #         self.__instance.set_progress(float(completed / len(self.__instance.available_ip_address)) * 100)
        self.__instance.finish_discovery()


@celery.current_app.task(name='DiscoveryTask', bind=True, base=DiscoveryTask)
def discovery_task(self, *args, **kwargs):
    return self.main(self, *args, **kwargs)
