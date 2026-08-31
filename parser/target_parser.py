class TargetParser:

    @staticmethod
    def parse(root):

        targets = []

        for target in root.findall("TARGET"):
            targets.append(
                target.attrib.get("NAME")
            )

        return targets