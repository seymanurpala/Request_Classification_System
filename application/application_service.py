import logging
from typing import List, Optional

import config
from domain.task.i_prediction_service import IPredictionService
from domain.task.task_service import TaskService
from domain.task_type.task_type_service import TaskTypeService

from application.dto.request.add_task_type_request import AddTaskTypeRequest
from application.dto.request.ai_prediction_request import AIPredictionRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.create_task_request import CreateTaskRequest
from application.dto.response.ai_prediction_response import AIPredictionResponse
from application.dto.response.task_response import TaskResponse
from application.dto.response.task_type_response import TaskTypeResponse
from application.dto_assembler import TaskDtoAssembler
from application.dto_disassembler import TaskDtoDisassembler

logger = logging.getLogger(__name__)


class AppService:

    def __init__(
        self,
        taskService: TaskService,
        taskTypeService: TaskTypeService,
        predictionService: IPredictionService,
        listLimit: int = 50,
    ):
        self._taskService = taskService
        self._taskTypeService = taskTypeService
        self._predictionService = predictionService
        self._listLimit = listLimit
        self._assembler = TaskDtoAssembler()
        self._disassembler = TaskDtoDisassembler()

    def _getAllTaskTypes(self):
        return self._taskTypeService.getAll()

    def _getAllTaskTypeNames(self) -> set[str]:
        return {taskType.value for taskType in self._getAllTaskTypes()}

    def _getSupportedTaskTypeNames(self) -> Optional[set[str]]:
        try:
            return self._predictionService.getSupportedTypes()
        except Exception:
            logger.exception("Modelde desteklenen talep tipleri okunamadi.")
            return None

    def _getSelectableTaskTypeNames(self) -> set[str]:
        allTaskTypeNames = self._getAllTaskTypeNames()
        supportedTaskTypeNames = self._getSupportedTaskTypeNames()
        return allTaskTypeNames if supportedTaskTypeNames is None else allTaskTypeNames & supportedTaskTypeNames

    def _sanitizePredictionResult(self, result: dict, selectableTaskTypeNames: set[str]) -> dict:
        if not selectableTaskTypeNames:
            return {"tip": None, "olasilik": 0.0, "top_k": []}

        topKTahminler = [
            tahmin for tahmin in result.get("top_k", [])
            if tahmin.get("tip") in selectableTaskTypeNames
        ]

        if result.get("tip") not in selectableTaskTypeNames:
            return {"tip": None, "olasilik": 0.0, "top_k": topKTahminler}

        return {
            "tip": result.get("tip"),
            "olasilik": result.get("olasilik", 0.0),
            "top_k": topKTahminler,
        }

    def _validateTaskType(self, tip: str, alan: str, selectableTaskTypeNames: set[str]) -> None:
        if tip and tip not in selectableTaskTypeNames:
            raise ValueError(f"Gecersiz {alan}: {tip}")

    def _validateRequiredText(self, value: str, alan: str, minLength: int = 1) -> None:
        if not value or not value.strip():
            raise ValueError(f"{alan} bos olamaz.")
        if len(value.strip()) < minLength:
            raise ValueError(f"{alan} cok kisa.")

    def _validateGelisKanali(self, gelisKanali: str) -> None:
        if gelisKanali not in set(config.VALID_CHANNELS):
            raise ValueError(f"Gecersiz gelis kanali: {gelisKanali}")

    def _ensureTaskExists(self, taskId: str) -> None:
        if self._taskService.getById(taskId) is None:
            raise ValueError(f"Task bulunamadi: {taskId}")

    def _validateCreateTaskData(self, data: dict, selectableTaskTypeNames: set[str]) -> None:
        for key, label, minLength in [
            ("talepMetni", "Talep metni", 3),
            ("vatandasAdi", "Vatandas adi", 2),
            ("ilce", "Ilce", 1),
            ("gelisKanali", "Gelis kanali", 1),
        ]:
            self._validateRequiredText(data[key], label, minLength=minLength)

        self._validateGelisKanali(data["gelisKanali"])

        if data.get("manuelTip"):
            self._validateTaskType(data["manuelTip"], "talep tipi", selectableTaskTypeNames)

    def getChannels(self) -> List[str]:
        return list(config.VALID_CHANNELS)

    def createTask(self, req: CreateTaskRequest) -> bool:
        try:
            data = self._disassembler.toCreateData(req)
            manuelTip = data.get("manuelTip")
            selectableTaskTypeNames = self._getSelectableTaskTypeNames()
            self._validateCreateTaskData(data, selectableTaskTypeNames)
            predictionData = {
                "tahminTipi": None,
                "tahminOlasiligi": None,
                "topKTahminler": [],
            }

            try:
                prediction = self._sanitizePredictionResult(
                    self._predictionService.predict(data["talepMetni"]),
                    selectableTaskTypeNames,
                )
                predictionData = {
                    "tahminTipi": prediction["tip"],
                    "tahminOlasiligi": prediction["olasilik"],
                    "topKTahminler": prediction["top_k"],
                }
            except ValueError as e:
                if not manuelTip:
                    raise
                logger.warning(
                    "AI tahmini alinamadi, manuel secim ile kayit devam ediyor: %s",
                    e,
                )
            except Exception:
                logger.exception("Beklenmeyen AI hatasi")
                return False

            if not manuelTip and not predictionData["tahminTipi"]:
                raise ValueError("Talep tipi belirlenemedi.")

            self._taskService.save(
                **data,
                **predictionData,
            )
            return True
        except ValueError as e:
            logger.error(f"Talep olusturma hatasi: {e}")
            return False
        except Exception:
            logger.exception("Beklenmeyen hata (createTask)")
            return False

    def listTasks(self, limit: int = None) -> List[TaskResponse]:
        tasks = self._taskService.getAll(limit if limit is not None else self._listLimit)
        return self._assembler.toResponseList(tasks)

    def approveTask(self, req: ApproveTaskRequest) -> bool:
        try:
            data = self._disassembler.toApproveData(req)
            self._validateRequiredText(data["taskId"], "Task id")
            self._validateRequiredText(data["onaylananTip"], "Onaylanan tip")
            self._ensureTaskExists(data["taskId"])
            selectableTaskTypeNames = self._getSelectableTaskTypeNames()
            self._validateTaskType(data["onaylananTip"], "onaylanan tip", selectableTaskTypeNames)
            self._taskService.approve(**data)
            return True
        except ValueError as e:
            logger.error(f"Onaylama hatasi: {e}")
            return False
        except Exception:
            logger.exception("Beklenmeyen hata (approveTask)")
            return False

    def predictWithAI(self, req: AIPredictionRequest) -> AIPredictionResponse:
        try:
            selectableTaskTypeNames = self._getSelectableTaskTypeNames()
            result = self._sanitizePredictionResult(
                self._predictionService.predict(req.metin),
                selectableTaskTypeNames,
            )
            return self._assembler.toPredictionResponse(result)
        except ValueError as e:
            logger.warning(f"AI tahmin hatasi: {e}")
            return AIPredictionResponse(tip=None, olasilik=0.0, topK=[])

    def getTaskTypes(self) -> List[TaskTypeResponse]:
        taskTypes = self._getAllTaskTypes()
        supportedTaskTypeNames = self._getSupportedTaskTypeNames()
        if supportedTaskTypeNames is not None:
            taskTypes = [
                taskType for taskType in taskTypes
                if taskType.value in supportedTaskTypeNames
            ]
        return self._assembler.toTaskTypeResponseList(
            taskTypes,
            supportedTaskTypeNames,
        )

    def getTaskTypesForSettings(self) -> List[TaskTypeResponse]:
        taskTypes = self._getAllTaskTypes()
        supportedTaskTypeNames = self._getSupportedTaskTypeNames()
        return self._assembler.toTaskTypeResponseList(
            taskTypes,
            supportedTaskTypeNames,
        )

    def addTaskType(self, req: AddTaskTypeRequest) -> bool:
        try:
            data = self._disassembler.toAddTaskTypeData(req)
            self._validateRequiredText(data["isim"], "Talep tipi")
            return self._taskTypeService.add(**data)
        except ValueError as e:
            logger.error(f"Talep tipi ekleme hatasi: {e}")
            return False
        except Exception:
            logger.exception("Beklenmeyen hata (addTaskType)")
            return False

    def deleteTaskType(self, isim: str) -> bool:
        try:
            temizIsim = (isim or "").strip()
            self._validateRequiredText(temizIsim, "Talep tipi")
            if self._taskService.isTaskTypeInUse(temizIsim):
                raise ValueError("Bu talep tipi mevcut kayitlarda kullanildigi icin silinemez.")
            return self._taskTypeService.delete(temizIsim)
        except ValueError as e:
            logger.error(f"Talep tipi silme hatasi: {e}")
            return False
        except Exception:
            logger.exception("Beklenmeyen hata (deleteTaskType)")
            return False
