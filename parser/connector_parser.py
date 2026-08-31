from models.connector import Connector


class ConnectorParser:

    @staticmethod
    def parse(root):

        connectors = []

        for connector in root.findall("CONNECTOR"):

            connectors.append(

                Connector(

                    from_instance=connector.attrib.get("FROMINSTANCE"),

                    from_field=connector.attrib.get("FROMFIELD"),

                    to_instance=connector.attrib.get("TOINSTANCE"),

                    to_field=connector.attrib.get("TOFIELD")

                )

            )

        return connectors