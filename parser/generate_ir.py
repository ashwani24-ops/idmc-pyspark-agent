from pathlib import Path

from parser.repository_parser import RepositoryParser
from parser.ir_writer import IRWriter


def main():

    # ----------------------------------------------------------
    # Project root
    # ----------------------------------------------------------

    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    # ----------------------------------------------------------
    # Input repository
    # ----------------------------------------------------------

    xml_file = (
        project_root
        / "repository"
        / "Synthetic_IDMC_Repository.xml"
    )

    # ----------------------------------------------------------
    # Output directory
    # ----------------------------------------------------------

    output_directory = (
        project_root
        / "output"
    )

    print()
    print("=" * 70)
    print("IDMC REPOSITORY → NORMALIZED IR")
    print("=" * 70)

    print(
        f"Input : {xml_file}"
    )

    print(
        f"Output: {output_directory}"
    )

    # ----------------------------------------------------------
    # Parse repository
    # ----------------------------------------------------------

    mappings = RepositoryParser.parse(
        xml_file
    )

    print()
    print(
        f"Mappings discovered: "
        f"{len(mappings)}"
    )

    # ----------------------------------------------------------
    # Write JSON
    # ----------------------------------------------------------

    output_files = IRWriter.write_all(
        mappings,
        output_directory
    )

    print()

    for output_file in output_files:

        print(
            f"Generated: {output_file}"
        )

    print()
    print(
        "IR generation completed successfully."
    )


if __name__ == "__main__":
    main()