from google.genai.types import FunctionCall


class LLMResponse:
    def __init__(
        self,
        text: str = "",
        action_task: list[FunctionCall] = None,
    ):
        self.text = text
        self.action_task = action_task