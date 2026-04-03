from abc import ABC, abstractmethod
from typing import Optional, List

from pymongo import DESCENDING
from bson import ObjectId, errors as bsonErrors

from domain.task.task import Task
from domain.task.task_factory import TaskFactory
from infrastructure.persistence.mongo_client import getDb
import config


class ITaskRepository(ABC):

    @abstractmethod
    def save(self, task: Task) -> str: ...

    @abstractmethod
    def getById(self, taskId: str) -> Optional[Task]: ...

    @abstractmethod
    def getAll(self, limit: int) -> List[Task]: ...

    @abstractmethod
    def count(self) -> int: ...


class TaskRepository(ITaskRepository):

    def __init__(self):
        self._col     = getDb()[config.MONGO_COLLECTION]
        self._factory = TaskFactory()

    def save(self, task: Task) -> str:
        data = self._factory.createObjectForDB(task)
        if task.id:
            try:
                result = self._col.update_one(
                    {"_id": ObjectId(task.id)},
                    {"$set": data}
                )
                if result.matched_count == 0:
                    raise ValueError(f"Task bulunamadı: {task.id}")
            except bsonErrors.InvalidId:
                raise ValueError(f"Geçersiz task id: {task.id}")
        else:
            result = self._col.insert_one(data)
            task.id = str(result.inserted_id)
        return task.id

    def getById(self, taskId: str) -> Optional[Task]:
        try:
            doc = self._col.find_one({"_id": ObjectId(taskId)})
            return self._factory.createObjectFromDB(doc) if doc else None
        except (bsonErrors.InvalidId, TypeError):
            return None

    def getAll(self, limit: int) -> List[Task]:
        cursor = (
            self._col.find()
            .sort("olusturmaTarihi", DESCENDING)
            .limit(limit)
        )
        return [self._factory.createObjectFromDB(doc) for doc in cursor]

    def count(self) -> int:
        return self._col.count_documents({})