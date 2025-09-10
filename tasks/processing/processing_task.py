import inspect
from abc import ABC, abstractmethod

from model.event import Event
from resources.load_config import load_config
from resources.logger import log, LogCategory


class ProcessingTask(ABC):
    def __init__(self, event: Event, prompt_name: str):
        self.event = event
        self.config = load_config()
        self.prompt_template = self._get_prompt_template(prompt_name)

    @property
    @abstractmethod
    def action_registry(self) -> dict:
        pass

    @abstractmethod
    def run(self):
        pass

    def build_action_tasks_list(self) -> str:
        lines = []
        for name, fn in self.action_registry.items():
            sig = inspect.signature(fn)
            params = ", ".join(f"{p.name}: {p.annotation.__name__ if p.annotation != inspect._empty else 'str'}"
                               for p in sig.parameters.values())
            lines.append(f"- {name}({params})")

        return "\n".join(lines)

    def _get_prompt_template(self, prompt_name) -> str:
        template = self.config.get(prompt_name)
        if not template:
            log("'prompt' key not found in config.yaml. Exiting.", LogCategory.END)
            raise SystemExit("Prompt template not found.")
        return template

    def create_prompt(self) -> str:
        try:
            prompt = self.prompt_template.format(
                processing_task_result=self.run(),
                action_tasks=self.build_action_tasks_list(),
            )
            log(prompt, LogCategory.USER)
            return prompt
        except KeyError as e:
            log(f"Error formatting prompt template. Missing key: {e}", LogCategory.END)
            print(f"Prompt Template: {self.prompt_template}")
            print("--------------------------------------")
            raise KeyError(
                f"Failed to format prompt. Check your 'prompt' in config.yaml."
            ) from e