from typing import Any, Dict

from pydantic import BaseModel


class Event(BaseModel):
    task_name: str
    data: Any
    metadata: Dict[str, Any] = {}