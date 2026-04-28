from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from domain.task.task import Task
from domain.task.task_repository import ITaskRepository


class TaskService:

    def __init__(self, taskRepository: ITaskRepository):
        self._repo = taskRepository

    def save(
        self,
        talepMetni: str,
        vatandasAdi: str,
        ilce: str,
        gelisKanali: str,
        manuelTip: Optional[str] = None,
        tahminTipi: Optional[str] = None,
        tahminOlasiligi: Optional[float] = None,
        topKTahminler: Optional[list] = None,
    ) -> bool:
        task = Task(
            talepMetni=talepMetni,
            vatandasAdi=vatandasAdi,
            ilce=ilce,
            gelisKanali=gelisKanali,
            manuelTip=manuelTip,
            tahminTipi=tahminTipi,
            tahminOlasiligi=tahminOlasiligi,
            topKTahminler=topKTahminler or [],
        )
        self._repo.save(task)
        return True

    def approve(self, taskId: str, onaylananTip: str) -> bool:
        task = self._repo.getById(taskId)
        if task is None:
            raise ValueError()

        task.onaylananTip = onaylananTip
        task.onaylandiMi = True
        task.guncellemeTarihi = datetime.now(timezone.utc)

        self._repo.save(task)
        return True

    def getAll(self, limit: int) -> List[Task]:
        return self._repo.getAll(limit)

    def getById(self, taskId: str) -> Optional[Task]:
        return self._repo.getById(taskId)

    def isTaskTypeInUse(self, isim: str) -> bool:
        return self._repo.isTaskTypeInUse(isim)
