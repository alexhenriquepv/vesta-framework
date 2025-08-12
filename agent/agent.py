import json
import yaml
from abc import ABC, abstractmethod
from typing import Dict, List, Any

from model.models import AgentResponse, UserPrompt, ChatMessage
from tools.tool_manager import ToolManager
from resources.logger import log, LogCategory


class Agent(ABC):
    """
    Abstract base class for an intelligent agent.

    This agent orchestrates a thinking-acting loop to solve user queries
    by leveraging a set of predefined tools.
    """

    def __init__(self):
        self.tool_manager = ToolManager()
        self.history: List[ChatMessage] = []
        self.conversation_limit = 10

        self.config = self._load_config()
        self.print_logs = self.config.get('print_logs', False)
        self.prompt_template = self._get_prompt_template()

    @staticmethod
    def _load_config() -> Dict[str, Any]:
        """Loads config.yaml and returns its content."""
        try:
            with open('resources/config.yaml', 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as e:
            log(f"Error loading config.yaml: {e}. Exiting.", LogCategory.END)
            raise SystemExit from e

    def _get_prompt_template(self) -> str:
        """Retrieves the 'react_prompt' template from the loaded config."""
        prompt_template = self.config.get('react_prompt')
        if not prompt_template:
            log("'react_prompt' key not found in config.yaml. Exiting.", LogCategory.END)
            raise SystemExit("Prompt template not found.")
        return prompt_template

    def _create_prompt(self, user_input: str) -> str:
        """Formats the loaded prompt template with dynamic data."""
        tools_desc = []
        for tool in self.tool_manager.get_tools():
            tools_desc.append(
                f"- Name: {tool.name}\n"
                f"  Description: {tool.description}\n"
                f"  Parameters: {tool.params}\n"
            )

        formatted_history = [f"{turn.role}: {turn.content}" for turn in self.history]

        try:
            prompt = self.prompt_template.format(
                tools_description='\n'.join(tools_desc),
                history='\n'.join(formatted_history),
                user_prompt=user_input,
            )
            return prompt
        except KeyError as e:
            log(f"Error formatting prompt template. Missing key: {e}", LogCategory.END)
            print(f"Prompt Template: {self.prompt_template}")
            print(f"Provided keys: 'tools_description', 'history', 'user_prompt'")
            print("--------------------------------------")
            raise KeyError(
                f"Failed to format prompt. Check your 'react_prompt' in config.yaml for an invalid placeholder.") from e

    @staticmethod
    def _parse_llm_response(llm_response: str) -> Dict[str, Any]:
        """
        Parses the LLM's response to extract Thought, Action, and Parameters.
        Assumes the LLM returns a structured JSON.
        --- CORRIGIDO: Retorna sempre um dicionário
        """
        try:
            cleaned_response = llm_response.strip().strip("`json\n").strip("`")
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            log(f"Failed to parse LLM JSON response: {e}", LogCategory.END)
            return {}

    @abstractmethod
    def _call_llm_for_response(self, prompt: str) -> str:
        """Abstract method to call the LLM and get its response."""
        pass

    def _thinking_step(self, user_input: str) -> Dict[str, Any]:
        """
        Represents the 'Thinking' phase.
        Calls the LLM to get a Thought and an Action.
        """
        prompt = self._create_prompt(user_input)
        llm_response = self._call_llm_for_response(prompt)
        parsed_response = self._parse_llm_response(llm_response)

        thought = parsed_response.get("thought", "No thought provided.")
        self.history.append(ChatMessage(role="assistant", content=f"Thought: {thought}"))

        if self.print_logs:
            log(f"Thought: {thought}", LogCategory.THOUGHT)

        return parsed_response.get("action", {})

    def _acting_step(self, action: Dict[str, Any]) -> None:
        """
        Represents the 'Acting' phase.
        Executes a tool based on the LLM's action.
        """
        action_name = action.get("name")
        action_params = action.get("parameters", {})

        if action_name:
            self.history.append(
                ChatMessage(role="assistant", content=f"Action: {action_name} with params {action_params}"))

            if self.print_logs:
                log(f"Action: {action_name} with params {action_params}", LogCategory.ACTION)

            tool_info = self.tool_manager.find_by_name(action_name)

            if tool_info:
                try:
                    observation = tool_info.function(**action_params)
                    self.history.append(ChatMessage(role="system", content=f"Observation: {observation}"))
                    if self.print_logs:
                        log(f"Observation: {observation}", LogCategory.OBSERVATION)
                except Exception as e:
                    self.history.append(ChatMessage(role="system", content=f"Observation: Tool failed with error: {e}"))
                    if self.print_logs:
                        log(f"Observation: Tool failed with error: {e}", LogCategory.OBSERVATION)
            else:
                self.history.append(ChatMessage(role="system", content="Observation: Tool not found."))
                if self.print_logs:
                    log("Observation: Tool not found.", LogCategory.OBSERVATION)
        else:
            self.history.append(ChatMessage(role="system", content="Observation: No valid action provided by the LLM."))
            if self.print_logs:
                log("Observation: No valid action provided by the LLM.", LogCategory.OBSERVATION)

    def handle_prompt(self, user_prompt: UserPrompt) -> AgentResponse:
        """
        Main method to handle a user prompt by orchestrating the ReAct loop.
        """
        self.history.append(ChatMessage(role="user", content=user_prompt.prompt))
        if self.print_logs:
            log(f"User Input: {user_prompt.prompt}", LogCategory.USER)

        iterations = 0

        while iterations < self.conversation_limit:
            iterations += 1

            action = self._thinking_step(user_prompt.prompt)

            # --- CORRIGIDO: Verificação da chave 'name' dentro do dicionário 'action' ---
            action_name = action.get("name")
            if action_name == "final_answer":
                final_message = action.get("parameters", {}).get("message", "No message provided.")
                return AgentResponse(message=final_message, user_prompt=user_prompt)

            self._acting_step(action)

        return AgentResponse(
            message="Conversation limit reached.",
            user_prompt=user_prompt,
        )