from typing import Callable

from pydantic import BaseModel


class UserPrompt(BaseModel):
    prompt: str

class AgentResponse:
    def __init__(
            self,
            message: str = None,
            user_prompt: UserPrompt = None,
    ):
        self.message = message
        self.user_prompt = user_prompt

class ToolInfo:
    """
        Represents an executable function reference to be used by Agent.

        Attributes:
            name (str): Unique name to visualized by LLM and users.
            description (str): Describes what the tool executes.
            params (List[str]): Parameters that LLL will try to extract.
            function (Callable): Callable Function implementation.
        """
    def __init__(
            self,
            name: str = None,
            description: str = None,
            params: list[str] = None,
            function: Callable = None,
    ):
        self.name = name
        self.description = description
        self.params = params
        self.function = function

class ChatMessage:
    """
        A chat message for use in the history.

        Attributes:
            role (str): user or assistance.
            content (str): Content of the message.
    """
    def __init__(
            self,
            role: str = None,
            content: str = None,
    ):
        self.role = role
        self.content = content