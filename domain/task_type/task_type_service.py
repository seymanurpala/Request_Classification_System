from typing import List

from domain.task_type.task_type_repository import ITaskTypeRepository
from domain.task_type.types import TaskType


class TaskTypeService:

    def __init__(self, repo: ITaskTypeRepository):
        self._repo = repo

    def getAll(self) -> List[TaskType]:
        return self._repo.getAll()

    def add(self, isim: str) -> bool:
        tip = TaskType(isim)
        return self._repo.add(tip)

    def delete(self, isim: str) -> bool:
        return self._repo.delete(isim)
