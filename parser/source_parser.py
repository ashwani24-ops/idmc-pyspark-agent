class SourceParser:

    @staticmethod
    def parse(root):

        sources = []

        for source in root.findall("SOURCE"):
            sources.append(
                source.attrib.get("NAME")
            )

        return sources