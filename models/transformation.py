from dataclasses import dataclass, field

from typing import List

from models.port import Port


@dataclass
class Transformation:

    name: str

    type: str

    ports: List[Port] = field(default_factory=list)