class PromptBuilder:

    @staticmethod
    def build(ir, transformation):

        return f"""
You are an expert PySpark engineer.

Generate ONLY PySpark code.

Mapping:
{ir["mapping"]}

Transformation Type:
{transformation["type"]}

Transformation Name:
{transformation["name"]}

Ports:
{transformation["ports"]}

Return only executable PySpark.
"""