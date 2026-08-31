from pathlib import Path

from parser.repository_parser import RepositoryParser


def main():

    project_root = Path(
        __file__
    ).resolve().parent.parent

    xml_file = (
        project_root
        / "repository"
        / "Synthetic_IDMC_Repository.xml"
    )

    mappings = RepositoryParser.parse(
        xml_file
    )

    print()
    print("=" * 70)
    print("IDMC REPOSITORY PARSER TEST")
    print("=" * 70)

    print(
        f"Mappings found: {len(mappings)}"
    )

    for mapping in mappings:

        print()
        print(
            f"Mapping: {mapping['name']}"
        )

        print(
            f"  Sources: "
            f"{len(mapping['sources'])}"
        )

        print(
            f"  Targets: "
            f"{len(mapping['targets'])}"
        )

        print(
            f"  Transformations: "
            f"{len(mapping['transformations'])}"
        )

        print(
            f"  Connectors: "
            f"{len(mapping['connectors'])}"
        )

        print()
        print("  Transformations:")

        for transformation in mapping[
            "transformations"
        ]:

            print(
                f"    - "
                f"{transformation['name']} "
                f"({transformation['type']})"
            )


if __name__ == "__main__":
    main()