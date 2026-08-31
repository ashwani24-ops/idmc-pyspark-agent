from pathlib import Path
import json

from planner.execution_planner import ExecutionPlanner



def main():

    project_root = (
        Path(__file__)
        .resolve()
        .parent.parent
    )


    ir_file = (
        project_root
        /
        "output"
        /
        "m_Sales_Customer_Load.json"
    )


    with open(
        ir_file,
        "r",
        encoding="utf-8"
    ) as file:

        ir = json.load(file)



    planner = ExecutionPlanner(
        ir
    )


    plan = planner.generate_plan()


    output_file = (
        project_root
        /
        "output"
        /
        "m_Sales_Customer_Load_plan.json"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            plan,
            file,
            indent=2
        )


    print(
        "Execution plan generated:"
    )

    print(
        output_file
    )


    for step in plan["steps"]:

        print(
            step["sequence"],
            step["name"],
            step["type"],
            step["depends_on"]
        )



if __name__ == "__main__":

    main()