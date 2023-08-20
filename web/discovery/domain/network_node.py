import dataclasses
import typing


@dataclasses.dataclass
class NetworkNode:
    firewall_detected: int = 0
    opened_ports: typing.List[int] = dataclasses.field(default_factory=list)
    filtered_ports: typing.List[int] = dataclasses.field(default_factory=list)
    closed_ports: typing.List[int] = dataclasses.field(default_factory=list)
    progress: float = 0
    port: int = 0

    def __str__(self):
        return f'F/W[{self.firewall_detected}], [{self.progress:.2f}]'
