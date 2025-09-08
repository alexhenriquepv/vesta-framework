from typing import Any

from model.event import Event
import tensorflow as tf
from scipy.signal import butter, filtfilt
from tasks.task_base import TaskBase


class PPGAuthTask(TaskBase):

    def __init__(self):
        self.model = tf.keras.models.load_model("resources/ppg-auth.keras")
        self.butter = butter
        self.filtfilt = filtfilt
        self.fs = 625
        self.window_size = 10
        self.sample_size = self.fs * self.window_size
        self.execution_result: dict[str, Any] = {}

    @property
    def description(self) -> str:
        return (
            "This task uses a pre-trained PPG Auth model to predict who is the patient. "
            "It return the patient name and the confidence of prediction"
        )

    @property
    def result(self) -> dict[str, Any]:
        return self.execution_result

    def butter_lowpass_filter(self, data, cutoff=15, order=4):
        nyq = 0.5 * self.fs
        normal_cutoff = cutoff / nyq
        b, a = self.butter(order, normal_cutoff, btype='low', analog=False)
        return self.filtfilt(b, a, data)

    def preprocess(self, ppg_values):
        filtered = self.butter_lowpass_filter(ppg_values, cutoff=15, order=4)
        if len(filtered) != self.fs:
            raise ValueError(f"Sample must have {self.fs} items.")
        arr = (filtered - filtered.mean()) / filtered.std()
        import numpy as np
        arr = np.expand_dims(arr, axis=(0, -1))
        return arr

    @staticmethod
    def find_patient_by_index(patient_index):
        if patient_index > 5:
            return "Jon Travolta"
        return "James Bond"

    def run(self, event: Event):
        x = self.preprocess(event.data)
        pred = self.model.predict(x)
        user_index = int(pred.argmax())
        confidence = float(pred.max())
        patient = self.find_patient_by_index(user_index)
        self.execution_result = {
            "confidence": confidence,
            "patient": patient,
        }
