from typing import Optional

from google import genai
from google.genai import types
from google.genai.types import FunctionCall

from tasks.ActionTasks.send_push_notification import send_push_notification_declaration
from tasks.ActionTasks.turn_alarm_on import turn_alarm_on_declaration

class LLMResponse:
    def __init__(
        self,
        text: str = "",
        action_task: list[FunctionCall] = None,
    ):
        self.text = text
        self.action_task = action_task

class GeminiLLM:
    def __init__(self):
        super().__init__()
        self.model_name = "gemini-2.5-flash-lite"
        self.client = genai.Client()
        tools = types.Tool(
            function_declarations=[
                turn_alarm_on_declaration,
                send_push_notification_declaration
            ]
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