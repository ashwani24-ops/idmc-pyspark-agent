import json
from pathlib import Path


class CopilotPromptGenerator:

    def __init__(self, ir_file, plan_file):
        self.ir_file = Path(ir_file)
        self.plan_file = Path(plan_file)

    def load_json(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def generate(self):

        ir = self.load_json(self.ir_file)
        plan = self.load_json(self.plan_file)

        mapping_name = ir.get(
            "name",
            "UNKNOWN_MAPPING"
        )

        prompt = f"""
# IDMC TO PYSPARK GENERATION TASK

You are an expert Informatica IDMC and
Databricks PySpark migration engineer.

Convert the supplied IDMC mapping metadata
into production-quality PySpark code.

IMPORTANT:

- Do not invent metadata.
- Do not invent fields.
- Do not invent transformations.
- Preserve transformation order.
- Preserve field lineage.
- Preserve business logic.

# MAPPING

{mapping_name}

# TRANSFORMATION RULES

SOURCE:
Use Spark DataFrame readers.

Use a placeholder:

SOURCE_PATH = "<SOURCE_PATH>"

FILTER:
Convert to DataFrame filter operations.

EXPRESSION:
Convert expressions into withColumn operations.

LOOKUP:
Convert lookup transformations into DataFrame joins.
Preserve lookup conditions and join type.

ROUTER:
Use when/otherwise or filtered DataFrames.
Preserve router conditions.

AGGREGATOR:
Use groupBy and agg.
Preserve grouping and aggregation functions.

SORTER:
Use orderBy.
Preserve sort direction.

TARGET:
Create the final target DataFrame.
Use:

TARGET_PATH = "<TARGET_PATH>"

Do not use real credentials.

# CODE QUALITY

The generated PySpark must:

- use Spark DataFrame APIs
- avoid pandas
- avoid unnecessary UDFs
- handle NULL values
- use meaningful DataFrame names
- use aliases for joins
- preserve IDMC transformation names in comments

For example:

# IDMC TRANSFORMATION: FIL_ACTIVE_CUSTOMER

# REQUIRED STRUCTURE

1. Imports
2. SparkSession
3. Configuration
4. Source reads
5. Transformations in execution order
6. Target preparation
7. Target write
8. Spark shutdown

# VALIDATION

Before producing the code verify:

1. Every source is represented.
2. Every transformation is represented.
3. Every target is represented.
4. Field lineage is respected.
5. Execution order is respected.
6. Target fields are populated.
7. No unknown fields are introduced.

If something cannot be translated exactly,
add a TODO comment rather than inventing behavior.

# IDMC IR

{json.dumps(ir, indent=2)}

# EXECUTION PLAN

{json.dumps(plan, indent=2)}

# FINAL OUTPUT

Generate only valid PySpark/Python code.

Do not provide explanations.
Do not provide Markdown fences.
Do not provide analysis.

The generated code should be saved as:

output/{mapping_name}.py
"""

        return prompt


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
        / "m_Sales_Customer_Load_prompt.md"
    )

    generator = CopilotPromptGenerator(
        ir_file,
        plan_file
    )

    prompt = generator.generate()

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(prompt)

    print()
    print("Copilot prompt generated successfully.")
    print()
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()