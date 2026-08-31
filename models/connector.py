from dataclasses import dataclass


@dataclass
class Connector:

    from_instance: str

    from_field: str

    to_instance: str

    to_field: str