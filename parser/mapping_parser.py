from models.mapping import Mapping

from parser.source_parser import SourceParser
from parser.target_parser import TargetParser
from parser.transformation_parser import TransformationParser
from parser.connector_parser import ConnectorParser


class MappingParser:

    @staticmethod
    def parse(root):

        mapping = Mapping(

            name=root.attrib.get("NAME", ""),

            description=root.attrib.get("DESCRIPTION", ""),

            folder=root.attrib.get("FOLDER", "")

        )

        mapping.sources = SourceParser.parse(root)

        mapping.targets = TargetParser.parse(root)

        mapping.transformations = TransformationParser.parse(root)

        mapping.connectors = ConnectorParser.parse(root)

        return mapping