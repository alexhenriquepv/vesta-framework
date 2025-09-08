from typing import Dict, Any

import yaml

from core.gemini import GeminiLLM
from model.agent_response import AgentResponse, Event
from resources.logger import log, LogCategory
from tasks.task_base import TaskBase


class Planner:

    def __init__(self):
        self.llm = GeminiLLM()
        self.config = self._load_config()
        self.prompt_template = self._get_prompt_template()

    @staticmethod
    def _load_config() -> Dict[str, Any]:
        try:
            with open('resources/config.yaml', 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as e:
            log(f"Error loading config.yaml: {e}. Exiting.", LogCategory.END)
            raise SystemExit from e

    def _get_prompt_template(self) -> str:
        prompt_template = self.config.get('prompt')
        if not prompt_template:
            log("'react_prompt' key not found in config.yaml. Exiting.", LogCategory.END)
            raise SystemExit("Prompt template not found.")
        return prompt_template

    def _create_prompt(self, task: TaskBase, event: Event) -> str:
        try:
            prompt = self.prompt_template.format(
                task_name=task.__class__.__name__,
                task_description=task.description,
                task_result=task.result,
                parameters=event.model_dump_json()
            )
            log(prompt, LogCategory.USER)
            return prompt
        except KeyError as e:
            log(f"Error formatting prompt template. Missing key: {e}", LogCategory.END)
            print(f"Prompt Template: {self.prompt_template}")
            print("--------------------------------------")
            raise KeyError(
                f"Failed to format prompt. Check your 'react_prompt' in config.yaml."
            ) from e

    def handle_task(self, task: TaskBase, event: Event) -> AgentResponse:
        prompt = self._create_prompt(task, event)
        llm_response = self.llm.generate_response(prompt)

        return AgentResponse(
            message=llm_response,
            event=event,
        )