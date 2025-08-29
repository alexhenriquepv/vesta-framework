import requests

from model.models import Event
from tasks.task_base import TaskBase


class GlycemiaLevelTask(TaskBase):

    def __init__(self):
        self.execution_result = ""

    @property
    def description(self) -> str:
        return (
            "This task calculates the glycemia level. "
            "It returns the glycemia value of patient and status classification. "
            "Can return the user profile and drug recommendations."
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

        self.execution_result = {
            "value": value,
            "status": status,
            "drug_recommendation": self.get_drug_recommendation(),
            "user_profile": self.get_user_profile(),
        }

    @staticmethod
    def get_user_profile() -> dict:
        url = "https://randomuser.me/api"
        response = requests.get(url)
        if response.ok:
            return response.json()
        else:
            return {}

    @staticmethod
    def get_drug_recommendation() -> dict:
        url = "https://api.fda.gov/drug/label.json?search=diabetes"
        response = requests.get(url)
        if response.ok:
            return response.json()
        else:
            return {}