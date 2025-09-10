from model.event import Event


class AgentResponse:
    def __init__(
            self,
            message: str = None,
            event: Event = None,
            executed_actions: list[dict] = None,
    ):
        self.message = message
        self.event = event
        self.executed_actions = executed_actions