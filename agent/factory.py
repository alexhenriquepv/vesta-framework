from agent.agent import Agent
from agent.gemini import AgentGemini


def create_agent(agent_type: str = "GEMINI") -> Agent:
    """
        Factory function to create an agent instance based on the specified type.

        Args:
            agent_type (str): The type of agent to create (e.g., "GEMINI").

        Returns:
            Agent: An instance of the requested agent.

        Raises:
            ValueError: If the agent_type is not supported.
        """
    if agent_type == "GEMINI":
        return AgentGemini()
    else:
        raise ValueError(f"'{agent_type}' is not a valid agent type.")