from model.event import Event
from resources.mocked_helpers import get_user_profile
from tasks.actions.alert_emergency_contact import alert_emergency_contact
from tasks.actions.send_push_notification import send_push_notification
from tasks.processing.processing_task import ProcessingTask


class GlycemiaLevelTask(ProcessingTask):

    def __init__(self, event: Event):
        super().__init__(event, prompt_name="glycemia_level")

    @property
    def action_registry(self):
        return {
            "alert_emergency_contact": alert_emergency_contact,
            "send_push_notification": send_push_notification,
        }

    def run(self):
        value = self.event.data
        if value > 180:
            status = "HIGH"
        elif value < 70:
            status = "LOW"
        else:
            status = "NORMAL"

        return {
            "value": value,
            "status": status,
            "user_profile": get_user_profile(),
        }