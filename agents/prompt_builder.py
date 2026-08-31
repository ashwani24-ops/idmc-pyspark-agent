import json


class PromptBuilder:

    @staticmethod
    def build(ir, execution_plan):

        prompt = f"""
You are an expert IDMC/Informatica to Databricks migration engineer.

Your task is to convert the supplied IDMC mapping
Intermediate Representation (IR) into production-quality
PySpark code.

IMPORTANT RULES

1. Follow the execution plan exactly.
2. Preserve the transformation sequence.
3. Preserve field-level mappings.
4. Preserve transformation expressions.
5. Preserve filter conditions.
6. Preserve lookup join conditions.
7. Preserve router conditions.
8. Preserve aggregator logic.
9. Preserve sorter logic.
10. Do not invent source or target fields.
11. Do not invent transformations.
12. Do not remove transformations.
13. Use PySpark DataFrame APIs.
14. Use Spark SQL only when it makes the generated
    code clearer.
15. Do not use pandas.
16. Add comments showing the original IDMC transformation.
17. Make the generated code readable and modular.
18. Handle NULL values appropriately.
19. Use aliases for joins where required.
20. The final target DataFrame must represent the
    IDMC target mapping.

IDMC MAPPING
============

{json.dumps(ir, indent=2)}


EXECUTION PLAN
==============

{json.dumps(execution_plan, indent=2)}


PYSPARK GENERATION REQUIREMENTS
===============================

Generate a complete PySpark program.

The program should include:

- SparkSession
- source DataFrame creation/reading
- transformation processing in execution order
- lookup joins
- expressions
- filters
- routers
- aggregations
- sorting
- target DataFrame creation
- final write section

For source and target locations, use clearly marked
placeholders such as:

SOURCE_PATH = "<SOURCE_PATH>"

TARGET_PATH = "<TARGET_PATH>"

Do not use real database credentials.

IMPORTANT OUTPUT FORMAT

Return ONLY valid Python/PySpark code.

Do not include:

- Markdown fences
- explanations
- introductory text
- analysis
- comments outside the Python code

The generated result must be directly saveable as a .py file.
"""

        return prompt