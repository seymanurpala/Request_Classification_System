from __future__ import annotations
from typing import Optional

from domain.task.task import Task


class TaskFactory:

    @staticmethod
    def create(
        talepMetni:      str,
        vatandasAdi:     str,
        ilce:            str,
        gelisKanali:     str,
        talepTipi:       Optional[str]   = None,
        tahminOlasiligi: Optional[float] = None,
        topKTahminler:   Optional[list]  = None,
    ) -> Task:
        return Task(
            talepMetni      = talepMetni,
            vatandasAdi     = vatandasAdi,
            ilce            = ilce,
            gelisKanali     = gelisKanali,
            tahminTipi      = talepTipi,
            tahminOlasiligi = tahminOlasiligi,
            topKTahminler   = topKTahminler or [],
        )

    @staticmethod
    def createObjectFromDB(data: dict) -> Optional[Task]:
        if not data:
            return None
        task = Task(
            talepMetni       = data.get("talepMetni"),
            vatandasAdi      = data.get("vatandasAdi"),
            ilce             = data.get("ilce"),
            gelisKanali      = data.get("gelisKanali"),
            tahminTipi       = data.get("tahminTipi"),
            tahminOlasiligi  = data.get("tahminOlasiligi"),
            topKTahminler    = data.get("topKTahminler", []),
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
            "tahminTipi":       task.tahminTipi,
            "tahminOlasiligi":  task.tahminOlasiligi,
            "topKTahminler":    task.topKTahminler or [],
            "onaylananTip":     task.onaylananTip,
            "onaylandiMi":      task.onaylandiMi,
            "olusturmaTarihi":  task.olusturmaTarihi,
            "guncellemeTarihi": task.guncellemeTarihi,
        }