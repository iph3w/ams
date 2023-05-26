import redis
import dataclasses
import threading
import json
import typing
import uuid

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
    def __init__(self, gid: uuid.UUID) -> None:
        self.__redis = redis.Redis()
        self.__lock: threading.Lock = threading.Lock()
        self.__nodes: typing.Dict = {}
        self.__edges: typing.List = []
        self.__uuid: uuid.UUID = gid
        try:
            if self.__redis.get(self.__uuid) is not None:
                tmp = json.loads(self.__redis.get(self.__uuid).decode("utf-8"))
                self.__nodes = tmp[NODES_INDEX]
                self.__edges = tmp[EDGES_INDEX]
        except:
            pass

    def add_node(self, node: NetworkNode, name: str, commit: bool = True):
        result = False
        with self.__lock:
            if node is not None:
                self.__nodes[name] = dataclasses.asdict(node)
                result = True
            else:
                if name not in self.__nodes.keys():
                    self.__nodes[name] = None
                    result = True
        if result is True and commit is True:
            self.save()
        return result

    def remove_node(self, name: str, commit: bool = True):
        result = False
        with self.__lock:
            if name in self.__nodes.keys():
                del self.__nodes[name]
                result = True
        if result is True and commit is True:
            self.save()
        return result

    def add_edge(self, node1: str, node2: str, commit: bool = True):
        result = False
        with self.__lock:
            if (node1, node2) not in self.__edges:
                self.__edges.append((node1, node2))
                result = True
        if result is True and commit is True:
            self.save()
        return result

    def save(self) -> (bool | None):
        return self.__redis.set(str(self.__uuid), self.to_json())

    def to_dict(self) -> typing.Dict:
        res = {}
        with self.__lock:
            res = {NODES_INDEX: self.__nodes, EDGES_INDEX: self.__edges}
        return res

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __str__(self):
        return str(self.__redis.get(str(self.__uuid)))
