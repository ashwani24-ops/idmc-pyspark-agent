import json
from pathlib import Path


class IRWriter:
    """
    Writes normalized mapping IR to JSON files.
    """

    @staticmethod
    def write_mapping(
        mapping,
        output_directory
    ):

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        mapping_name = mapping.get(
            "name",
            "UNKNOWN_MAPPING"
        )

        output_file = (
            output_directory
            / f"{mapping_name}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                mapping,
                file,
                indent=2
            )

        return output_file

    @staticmethod
    def write_all(
        mappings,
        output_directory
    ):

        output_files = []

        for mapping in mappings:

            output_file = (
                IRWriter.write_mapping(
                    mapping,
                    output_directory
                )
            )

            output_files.append(
                output_file
            )

        return output_files