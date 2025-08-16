from core.planner import Planner
from model.models import Event
from tasks.glycemia_level_task import GlycemiaLevelTask
from tasks.ppg_auth_task import PPGAuthTask


class EventOrchestrator:
    def __init__(self):
        self.planner = Planner()
        self.tasks = [
            GlycemiaLevelTask,
            PPGAuthTask
        ]

    def handle_event(self, event: Event):
        for task in self.tasks:
            if task.__name__ == event.task_name:
                task_instance = task()
                task_instance.run(event)
                return self.planner.handle_task(task_instance, event)

        return {"error": f'Task requested not found {event.task_name}'}