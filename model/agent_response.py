from model.event import Event


class AgentResponse:
    def __init__(
            self,
            message: str = None,
            event: Event = None,
    ):
        self.message = message
        self.event = event