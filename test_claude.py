from agents.claude_client import ClaudeClient


def main():

    client = ClaudeClient()

    prompt = """
You are a Databricks PySpark expert.

Write a simple PySpark example
that creates a DataFrame with
customer_id and customer_name.

Return only the PySpark code.
"""

    response = client.generate(prompt)

    print()
    print("========== CLAUDE RESPONSE ==========")
    print(response)
    print("=====================================")


if __name__ == "__main__":
    main()