import json
from pathlib import Path

from validator.pyspark_validator import (
    PySparkValidator
)


def main():

    project_root = (
        Path(__file__)
        .resolve()
        .parent.parent
    )

    ir_file = (
        project_root
        / "output"
        / "m_Sales_Customer_Load.json"
    )

    plan_file = (
        project_root
        / "output"
        / "m_Sales_Customer_Load_plan.json"
    )

    pyspark_file = (
        project_root
        / "output"
        / "m_Sales_Customer_Load.py"
    )

    # --------------------------------------------------
    # Read IR
    # --------------------------------------------------

    with open(
        ir_file,
        "r",
        encoding="utf-8"
    ) as file:

        ir = json.load(file)

    # --------------------------------------------------
    # Read execution plan
    # --------------------------------------------------

    with open(
        plan_file,
        "r",
        encoding="utf-8"
    ) as file:

        execution_plan = json.load(file)

    # --------------------------------------------------
    # Read generated PySpark
    # --------------------------------------------------

    with open(
        pyspark_file,
        "r",
        encoding="utf-8"
    ) as file:

        pyspark_code = file.read()

    # --------------------------------------------------
    # Validate
    # --------------------------------------------------

    validator = PySparkValidator(
        ir,
        execution_plan,
        pyspark_code
    )

    result = validator.validate()

    # --------------------------------------------------
    # Report
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("PYSPARK MIGRATION VALIDATION")
    print("=" * 70)

    print()
    print(
        f"Mapping: {ir.get('name')}"
    )

    print()

    for item in result["results"]:

        print(
            f"[{item['status']}] "
            f"{item['check']}"
        )

    if result["warnings"]:

        print()
        print("WARNINGS")

        for warning in result["warnings"]:

            print(
                f"  - {warning}"
            )

    if result["errors"]:

        print()
        print("ERRORS")

        for error in result["errors"]:

            print(
                f"  - {error}"
            )

    print()

    if result["valid"]:

        print("STATUS: VALID")

    else:

        print("STATUS: INVALID")

    print("=" * 70)


if __name__ == "__main__":

    main()