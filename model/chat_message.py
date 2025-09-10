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