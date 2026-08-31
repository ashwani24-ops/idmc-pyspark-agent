from pathlib import Path

from generator.ir_reader import IRReader
from generator.transformation_planner import TransformationPlanner


def main():

    project_root = Path(__file__).resolve().parent.parent

    ir_file = project_root / "output" / "Customer_Load.json"

    ir = IRReader.read(ir_file)

    plan = TransformationPlanner.create_plan(ir)

    print("\nTransformation Plan")
    print("=" * 60)

    for step in plan:

        operation = step["operation"]

        print(
            f"\nStep {step['step']}: {operation}"
        )

        if operation == "READ":

            print(
                f"    Object: {step['object']}"
            )

        elif operation == "TRANSFORMATION":

            print(
                f"    Name: {step['name']}"
            )

            print(
                f"    Type: {step['type']}"
            )

            for port in step.get("ports", []):

                print(
                    f"    Port: {port['name']}"
                )

                print(
                    f"    Expression: "
                    f"{port.get('expression')}"
                )

        elif operation == "WRITE":

            print(
                f"    Object: {step['object']}"
            )


if __name__ == "__main__":
    main()