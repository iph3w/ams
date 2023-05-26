import dataclasses
import json
import typing

NODES_INDEX = "NODES"
EDGES_INDEX = "EDGES"


@dataclasses.dataclass
class NetworkNode:
    firewall_detected: bool = False
    opened_ports: typing.List[int] = dataclasses.field(default_factory=list)
    filtered_ports: typing.List[int] = dataclasses.field(default_factory=list)
    closed_ports: typing.List[int] = dataclasses.field(default_factory=list)
    progress: float = 0
    port: int = 0

    def __str__(self):
        return f'F/W[{self.firewall_detected}], [{self.progress:.2f}]'


class NetworkGraph:
    __nodes: typing.Dict = {}
    __edges: typing.List = []

    def add_node(self, node: NetworkNode, name: str):
        if node is not None:
            self.__nodes[name] = dataclasses.asdict(node)
            return True
        else:
            if name not in self.__nodes.keys():
                self.__nodes[name] = None
                return True
        return False

    def remove_node(self, name: str):
        if name in self.__nodes.keys():
            del self.__nodes[name]
            return True
        return False

    def add_edge(self, node1: str, node2: str):
        if (node1, node2) not in self.__edges:
            self.__edges.append((node1, node2))
            return True
        return False

    def to_dict(self) -> typing.Dict:
        return {NODES_INDEX: self.__nodes, EDGES_INDEX: self.__edges}
