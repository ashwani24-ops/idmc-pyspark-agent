class RepositorySummary:

    @staticmethod
    def print(mappings):

        print()

        print("Repository Summary")

        print("------------------")

        print(f"Mappings : {len(mappings)}")

        transformations = 0

        connectors = 0

        sources = 0

        targets = 0

        for mapping in mappings:

            transformations += len(mapping.transformations)

            connectors += len(mapping.connectors)

            sources += len(mapping.sources)

            targets += len(mapping.targets)

        print(f"Sources : {sources}")

        print(f"Targets : {targets}")

        print(f"Transformations : {transformations}")

        print(f"Connectors : {connectors}")