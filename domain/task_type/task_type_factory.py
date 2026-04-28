from __future__ import annotations
from typing import Optional

from domain.task_type.types import TaskType


class TaskTypeFactory:

    @staticmethod
    def createObjectFromDB(data: dict) -> Optional[TaskType]:
        if not data:
            return None
        return TaskType(data["isim"])

    @staticmethod
    def createObjectForDB(taskType: TaskType) -> dict:
        return {"isim": taskType.value}
