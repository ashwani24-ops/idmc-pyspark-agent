from pathlib import Path
import json

from parser.ir_validator import IRValidator


def main():

    project_root = (
        Path(__file__).resolve().parent.parent
    )

    output_directory = project_root / "output"

    json_files = sorted(
        output_directory.glob("*.json")
    )

    if not json_files:
        print("No JSON files found in output/")
        return

    overall_valid = True

    for json_file in json_files:

        print()
        print("=" * 80)
        print(f"FILE: {json_file.name}")
        print("=" * 80)

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:
            ir = json.load(file)

        print(f"Mapping: {ir.get('name')}")

        validator = IRValidator(ir)

        result = validator.validate()

        print()
        print("ERRORS:")
        
        if result["errors"]:
            for i, error in enumerate(
                result["errors"],
                start=1
            ):
                print(f"{i}. {error}")
        else:
            print("None")

        print()
        print("WARNINGS:")

        if result["warnings"]:
            for i, warning in enumerate(
                result["warnings"],
                start=1
            ):
                print(f"{i}. {warning}")
        else:
            print("None")

        print()
        print(
            "STATUS:",
            "VALID" if result["valid"]
            else "INVALID"
        )

        if not result["valid"]:
            overall_valid = False

    print()
    print("=" * 80)

    if overall_valid:
        print("ALL IR FILES ARE VALID")
    else:
        print("IR VALIDATION FAILED")

    print("=" * 80)


if __name__ == "__main__":
    main()