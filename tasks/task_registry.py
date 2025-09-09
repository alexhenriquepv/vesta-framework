from typing import List, Type

from google.genai import types


class TaskRegistry:
    processing_tasks: List[Type] = []
    action_tasks: List[types.FunctionDeclaration] = []

    @classmethod
    def register_processing(cls, task_cls: Type):
        cls.processing_tasks.append(task_cls)

    @classmethod
    def register_action(cls, declaration: types.FunctionDeclaration):
        cls.action_tasks.append(declaration)

    @classmethod
    def get_processing_tasks(cls):
        return cls.processing_tasks

    @classmethod
    def get_action_tasks(cls):
        return cls.action_tasks
