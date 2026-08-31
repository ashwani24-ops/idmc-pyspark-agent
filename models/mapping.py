from dataclasses import dataclass, field

from typing import List


@dataclass
class Mapping:

    name: str

    description: str = ""

    folder: str = ""

    sources: List[str] = field(default_factory=list)

    targets: List[str] = field(default_factory=list)

    transformations: List = field(default_factory=list)

    connectors: List = field(default_factory=list)