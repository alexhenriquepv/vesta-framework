from model.event import Event
from resources.mocked_helpers import get_user_profile
from tasks.actions.send_push_notification import send_push_notification
from tasks.processing.processing_task import ProcessingTask


class LowBatteryTask(ProcessingTask):

    def __init__(self, event: Event):
        super().__init__(event=event, prompt_name="low_battery")

    @property
    def action_registry(self) -> dict:
        return {
            "send_push_notification": send_push_notification,
        }

    def run(self):
        return {
            "battery_levels": self.event.data,
            "user_profile": get_user_profile()
        }