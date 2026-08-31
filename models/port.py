from dataclasses import dataclass


@dataclass
class Port:

    name: str

    datatype: str

    port_type: str

    expression: str = ""