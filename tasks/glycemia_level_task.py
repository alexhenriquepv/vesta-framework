from typing import Any

from model.models import Event
from tasks.task_base import TaskBase


class GlycemiaLevelTask(TaskBase):

    def __init__(self):
        self.execution_result = ""

    @property
    def description(self) -> str:
        return (
            "This task calculates the glycemia level. "
            "It returns the glycemia value of patient and status classification"
        )

    @property
    def result(self) -> str:
        return self.execution_result

    def run(self, event: Event):
        value = event.data
        if value > 180:
            status = "HIGH"
        elif value < 70:
            status = "LOW"
        else:
            status = "NORMAL"
        self.execution_result = {"value": value, "status": status}