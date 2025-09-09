from core.planner import Planner
from model.event import Event
from tasks.task_registry import TaskRegistry


class EventOrchestrator:
    def __init__(self):
        self.planner = Planner()
        self.processing_tasks = TaskRegistry.get_processing_tasks()

    def handle_event(self, event: Event):
        for task in self.processing_tasks:
            if task.__name__ == event.task_name:
                task_instance = task(event)
                return self.planner.handle_task(task_instance)

        return {"error": f'Task requested not found {event.task_name}'}