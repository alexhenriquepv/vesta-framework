import random

from model.event import Event
from tasks.actions.send_push_notification import send_push_notification
from tasks.actions.turn_alarm_on import turn_alarm_on
from tasks.processing.processing_task import ProcessingTask


class MovementDetectionTask(ProcessingTask):

    def __init__(self, event: Event):
        super().__init__(event=event, prompt_name="movement_detection")

    @property
    def action_registry(self):
        return {
            "turn_alarm_on": turn_alarm_on,
            "send_push_notification": send_push_notification,
        }

    def run(self) -> dict:
        object_detected = self.predict_object()
        return {
            "object_detected": object_detected
        }

    @staticmethod
    def predict_object():
        objects = ["cat", "pigeon", "person", "rat", "ball", "kite"]
        return random.choice(objects)