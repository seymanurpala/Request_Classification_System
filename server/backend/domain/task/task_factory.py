from __future__ import annotations
from typing import Optional

from domain.task.task import Task


class TaskFactory:

    @staticmethod
    def createObjectFromDB(data: dict) -> Optional[Task]:
        if not data:
            return None
        task = Task(
            talepMetni       = data.get("talepMetni"),
            vatandasAdi      = data.get("vatandasAdi"),
            ilce             = data.get("ilce"),
            gelisKanali      = data.get("gelisKanali"),
            manuelTip        = data.get("manuelTip"),
            tahminTipi       = data.get("tahminTipi"),
            tahminOlasiligi  = data.get("tahminOlasiligi"),
            topKTahminler    = data.get("topKTahminler") or [],
            onaylananTip     = data.get("onaylananTip"),
            onaylandiMi      = data.get("onaylandiMi", False),
            olusturmaTarihi  = data.get("olusturmaTarihi"),
            guncellemeTarihi = data.get("guncellemeTarihi"),
        )
        task.id = str(data["_id"]) if data.get("_id") else None
        return task

    @staticmethod
    def createObjectForDB(task: Task) -> dict:
        return {
            "talepMetni":       task.talepMetni,
            "vatandasAdi":      task.vatandasAdi,
            "ilce":             task.ilce,
            "gelisKanali":      task.gelisKanali,
            "manuelTip":        task.manuelTip,
            "tahminTipi":       task.tahminTipi,
            "tahminOlasiligi":  task.tahminOlasiligi,
            "topKTahminler":    task.topKTahminler or [],
            "onaylananTip":     task.onaylananTip,
            "onaylandiMi":      task.onaylandiMi,
            "olusturmaTarihi":  task.olusturmaTarihi,
            "guncellemeTarihi": task.guncellemeTarihi,
        }
