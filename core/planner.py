from core.gemini import GeminiLLM
from model.agent_response import AgentResponse, Event
from tasks.ProcessingTasks.processing_task import ProcessingTask


class Planner:

    def __init__(self):
        self.llm = GeminiLLM()

    def handle_task(self, processing_task: ProcessingTask) -> AgentResponse:
        prompt = processing_task.create_prompt()
        llm_response = self.llm.generate_response(prompt)
        action_tasks = llm_response.action_task
        executed_actions = []

        for task in action_tasks:
            response = processing_task.action_registry[task.name](**task.args)
            executed_actions.append({ "name": task.name, "response": response })

        return AgentResponse(
            message=llm_response.text,
            event=processing_task.event,
            executed_actions=executed_actions,
        )