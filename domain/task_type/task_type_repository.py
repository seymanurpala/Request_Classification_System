from abc import ABC, abstractmethod
from typing import List

from domain.task_type.task_type_factory import TaskTypeFactory
from domain.task_type.types import TaskType
from infrastructure.persistence.mongo_client import getDb
import config


class ITaskTypeRepository(ABC):

    @abstractmethod
    def getAll(self) -> List[TaskType]: ...

    @abstractmethod
    def add(self, taskType: TaskType) -> bool: ...

    @abstractmethod
    def delete(self, isim: str) -> bool: ...


class TaskTypeRepository(ITaskTypeRepository):

    def __init__(self):
        self._col = getDb()[config.TASK_TYPE_COLLECTION]
        self._factory = TaskTypeFactory()

    def getAll(self) -> List[TaskType]:
        return [self._factory.createObjectFromDB(d) for d in self._col.find()]

    def add(self, taskType: TaskType) -> bool:
        if self._col.find_one({"isim": taskType.value}):
            return False
        self._col.insert_one(self._factory.createObjectForDB(taskType))
        return True

    def delete(self, isim: str) -> bool:
        return self._col.delete_one({"isim": isim}).deleted_count > 0
