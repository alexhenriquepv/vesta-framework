from abc import ABC

from google import genai

from agent.agent import Agent


class AgentGemini(Agent, ABC):
    def __init__(self):
        super().__init__()
        self.model_name = "gemini-2.5-flash-lite"
        self.client = genai.Client()

    def _call_llm_for_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text