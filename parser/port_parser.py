from models.port import Port


class PortParser:

    @staticmethod
    def parse(transformation_node):

        ports = []

        for port in transformation_node.findall("PORT"):

            ports.append(

                Port(

                    name=port.attrib.get("NAME"),

                    datatype=port.attrib.get("DATATYPE"),

                    port_type=port.attrib.get("PORTTYPE"),

                    expression=port.attrib.get("EXPRESSION", "")

                )

            )

        return ports