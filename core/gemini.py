from google import genai
from google.genai import types

from model.llm_response import LLMResponse
from tasks.task_registry import TaskRegistry


class GeminiLLM:
    def __init__(self):
        super().__init__()
        self.model_name = "gemini-2.5-flash-lite"
        self.client = genai.Client()
        tools = types.Tool(
            function_declarations=TaskRegistry.get_action_tasks()
        )
        self.config = types.GenerateContentConfig(tools=[tools])

    def generate_response(self, prompt: str) -> LLMResponse:

        contents = [
            types.Content(
                role="user", parts=[types.Part(text=prompt)]
            )
        ]

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=self.config,
        )

        text_response = ""
        function_call: list[types.FunctionCall] = []

        if response.candidates[0].content.parts:
            parts = response.candidates[0].content.parts
            for part in parts:
                if getattr(part, "text", None):
                    text_response += part.text
                if getattr(part, "function_call", None):
                    function_call.append(part.function_call)

        return LLMResponse(text_response, function_call)