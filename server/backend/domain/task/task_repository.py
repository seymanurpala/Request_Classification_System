from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId, errors as bsonErrors
from pymongo import DESCENDING

import config
from domain.task.task import Task
from domain.task.task_factory import TaskFactory
from infrastructure.persistence.mongo_client import getDb


class ITaskRepository(ABC):

    @abstractmethod
    def save(self, task: Task) -> None: ...

    @abstractmethod
    def getById(self, taskId: str) -> Optional[Task]: ...

    @abstractmethod
    def getAll(self, limit: int) -> List[Task]: ...

    @abstractmethod
    def isTaskTypeInUse(self, isim: str) -> bool: ...


class TaskRepository(ITaskRepository):

    def __init__(self):
        self._col = getDb()[config.MONGO_COLLECTION]
        self._factory = TaskFactory()

    def save(self, task: Task) -> None:
        data = self._factory.createObjectForDB(task)
        if task.id:
            try:
                objectId = ObjectId(task.id)
            except (bsonErrors.InvalidId, TypeError):
                raise ValueError()

            result = self._col.update_one(
                {"_id": objectId},
                {"$set": data},
            )
            if result.matched_count == 0:
                raise ValueError()
        else:
            result = self._col.insert_one(data)
            task.id = str(result.inserted_id)

    def getById(self, taskId: str) -> Optional[Task]:
        try:
            objectId = ObjectId(taskId)
        except (bsonErrors.InvalidId, TypeError):
            return None

        doc = self._col.find_one({"_id": objectId})
        return self._factory.createObjectFromDB(doc) if doc else None

    def getAll(self, limit: int) -> List[Task]:
        cursor = (
            self._col.find()
            .sort("olusturmaTarihi", DESCENDING)
            .limit(limit)
        )
        return [self._factory.createObjectFromDB(doc) for doc in cursor]

    def isTaskTypeInUse(self, isim: str) -> bool:
        return self._col.find_one(
            {
                "$or": [
                    {"manuelTip": isim},
                    {"tahminTipi": isim},
                    {"onaylananTip": isim},
                ]
            },
            {"_id": 1},
        ) is not None
