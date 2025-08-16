from abc import ABC, abstractmethod
from typing import Any


class TaskBase(ABC):

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def result(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def run(self, event):
        pass

