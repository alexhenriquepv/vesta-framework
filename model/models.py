from typing import Callable, Any, Dict

from pydantic import BaseModel

from model.event import Event


class UserPrompt(BaseModel):
    prompt: str


class AgentResponse:
    def __init__(
            self,
            message: str = None,
            event: Event = None,
    ):
        self.message = message
        self.event = event


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
            function: Callable = None,
    ):
        self.name = name
        self.description = description
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
