import os

from dotenv import load_dotenv
from anthropic import Anthropic



class ClaudeClient:

    def __init__(self):

        # Load .env from project root
        load_dotenv()

        api_key = os.getenv(
            "ANTHROPIC_API_KEY"
        )

        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not found. "
                "Check your .env file."
            )

        self.client = Anthropic(
            api_key=api_key
        )

    def generate(self, prompt):

        response = self.client.messages.create(

            # Use the Claude model available to your API account.
            model="claude-sonnet-4-20250514",

            max_tokens=2000,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text