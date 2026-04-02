from typing import List

from domain.task_type.types import TaskType
from domain.task_type.task_type_factory import TaskTypeFactory
from domain.task_type.task_type_repository import ITaskTypeRepository


class TaskTypeService:

    def __init__(self, repo: ITaskTypeRepository):
        self._repo    = repo
        self._factory = TaskTypeFactory()

    def getAll(self) -> List[TaskType]:
        return self._repo.getAll()

    def add(self, isim: str) -> bool:
        tip = self._factory.create(isim)
        return self._repo.add(tip)

    def delete(self, isim: str) -> bool:
        return self._repo.delete(isim)
