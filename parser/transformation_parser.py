from parser.port_parser import PortParser

from models.transformation import Transformation


class TransformationParser:

    @staticmethod
    def parse(root):

        transformations = []

        for node in root.findall("TRANSFORMATION"):

            transformation = Transformation(

                name=node.attrib.get("NAME"),

                type=node.attrib.get("TYPE")

            )

            transformation.ports = PortParser.parse(node)

            transformations.append(transformation)

        return transformations