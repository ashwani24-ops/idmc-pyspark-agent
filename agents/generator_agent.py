from agents.prompt_builder import PromptBuilder


class GeneratorAgent:

    def __init__(self):
        pass


    def generate_prompt(self, ir, execution_plan):

        prompt = PromptBuilder.build(
            ir,
            execution_plan
        )

        return prompt