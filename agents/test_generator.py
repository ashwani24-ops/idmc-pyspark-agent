import json
from pathlib import Path

from agents.generator_agent import GeneratorAgent


def main():

    project_root = (
        Path(__file__).resolve().parent.parent
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

    output_file = (
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

    print()
    print("Starting Claude PySpark generation...")
    print()

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    agent = GeneratorAgent()

    code = agent.generate_prompt(
        ir,
        execution_plan
    )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(code)

    print(
        "PySpark generated successfully."
    )

    print()
    print(
        f"Output: {output_file}"
    )

    print()
    print(
        "Generated code preview:"
    )

    print("-" * 70)

    print(
        code[:3000]
    )

    print("-" * 70)


if __name__ == "__main__":
    main()