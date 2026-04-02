from __future__ import annotations
from typing import Optional, List
from datetime import datetime, timezone

from domain.task.task import Task
from domain.task.task_factory import TaskFactory
from domain.task.task_repository import ITaskRepository


class TaskService:

    def __init__(self, taskRepository: ITaskRepository):
        self._repo    = taskRepository
        self._factory = TaskFactory()

    def save(
        self,
        talepMetni:      str,
        vatandasAdi:     str,
        ilce:            str,
        gelisKanali:     str,
        talepTipi:       Optional[str]   = None,
        tahminOlasiligi: Optional[float] = None,
        topKTahminler:   Optional[list]  = None,
    ) -> Task:
        task = self._factory.create(
            talepMetni      = talepMetni,
            vatandasAdi     = vatandasAdi,
            ilce            = ilce,
            gelisKanali     = gelisKanali,
            talepTipi       = talepTipi,
            tahminOlasiligi = tahminOlasiligi,
            topKTahminler   = topKTahminler or [],
        )
        self._repo.save(task)
        return task

    def approve(self, taskId: str, onaylananTip: str) -> Task:
        task = self._repo.getById(taskId)
        if task is None:
            raise ValueError(f"Task bulunamadı: {taskId}")

        task.onaylananTip     = onaylananTip
        task.onaylandiMi      = True
        task.guncellemeTarihi = datetime.now(timezone.utc)

        self._repo.save(task)
        return task

    def getAll(self, limit: int) -> List[Task]:
        return self._repo.getAll(limit)

    def getById(self, taskId: str) -> Optional[Task]:
        return self._repo.getById(taskId)

    def count(self) -> int:
        return self._repo.count()