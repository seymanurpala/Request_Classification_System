import logging
from typing import List

from domain.task.task_service import TaskService
from domain.task.i_prediction_service import IPredictionService
from domain.task_type.task_type_service import TaskTypeService
from domain.task_type.types import TaskType

from application.dto.request.create_task_request import CreateTaskRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.ai_prediction_request import AIPredictionRequest
from application.dto.request.add_task_type_request import AddTaskTypeRequest
from application.dto.response.task_response import TaskResponse
from application.dto.response.ai_prediction_response import AIPredictionResponse
from application.dto_assembler import TaskDtoAssembler
from application.dto_disassembler import TaskDtoDisassembler

logger = logging.getLogger(__name__)


class AppService:

    def __init__(
        self,
        taskService:       TaskService,
        taskTypeService:   TaskTypeService,
        predictionService: IPredictionService,
        listLimit:         int = 50,
    ):
        self._taskService       = taskService
        self._taskTypeService   = taskTypeService
        self._predictionService = predictionService
        self._listLimit         = listLimit
        self._assembler         = TaskDtoAssembler()
        self._disassembler      = TaskDtoDisassembler()

    def _getValidTaskTypeNames(self) -> set[str]:
        return {taskType.value for taskType in self._taskTypeService.getAll()}

    def _validateTaskType(self, tip: str, alan: str) -> None:
        if tip and tip not in self._getValidTaskTypeNames():
            raise ValueError(f"Geçersiz {alan}: {tip}")

    def createTask(self, req: CreateTaskRequest) -> bool:
        try:
            data = self._assembler.toCreateData(req)
            manuelTip = data.get("talepTipi")

            if manuelTip:
                self._validateTaskType(manuelTip, "talep tipi")

            tahminTipi = None
            tahminOlasiligi = None
            topKTahminler = []

            try:
                prediction = self._predictionService.predict(data["talepMetni"])
                tahminTipi = prediction["tip"]
                tahminOlasiligi = prediction["olasilik"]
                topKTahminler = prediction["top_k"]
            except ValueError:
                if not manuelTip:
                    raise
                logger.warning("AI tahmini alınamadı, manuel seçim ile kayıt devam ediyor.")

            self._taskService.save(
                talepMetni      = data["talepMetni"],
                vatandasAdi     = data["vatandasAdi"],
                ilce            = data["ilce"],
                gelisKanali     = data["gelisKanali"],
                manuelTip       = manuelTip,
                tahminTipi      = tahminTipi,
                tahminOlasiligi = tahminOlasiligi,
                topKTahminler   = topKTahminler,
            )
            return True
        except ValueError as e:
            logger.error(f"Talep oluşturma hatası: {e}")
            return False
        except Exception as e:
            logger.error(f"Beklenmeyen hata (createTask): {e}")
            return False

    def listTasks(self, limit: int = None) -> List[TaskResponse]:
        try:
            tasks = self._taskService.getAll(limit if limit is not None else self._listLimit)
            return self._disassembler.toResponseList(tasks)
        except Exception as e:
            logger.error(f"Listeleme hatası: {e}")
            return []

    def countTasks(self) -> int:
        try:
            return self._taskService.count()
        except Exception as e:
            logger.error(f"Sayım hatası: {e}")
            return 0

    def approveTask(self, req: ApproveTaskRequest) -> bool:
        try:
            taskId, onaylananTip = self._assembler.toApproveData(req)
            self._validateTaskType(onaylananTip, "onaylanan tip")
            self._taskService.approve(taskId, onaylananTip)
            return True
        except ValueError as e:
            logger.error(f"Onaylama hatası: {e}")
            return False
        except Exception as e:
            logger.error(f"Beklenmeyen hata (approveTask): {e}")
            return False

    def predictWithAI(self, req: AIPredictionRequest) -> AIPredictionResponse:
        try:
            result = self._predictionService.predict(req.metin)
            return self._disassembler.toPredictionResponse(result)
        except ValueError as e:
            logger.error(f"AI tahmin hatası: {e}")
            return AIPredictionResponse(tip="Diğer", olasilik=0.0)
        except Exception as e:
            logger.error(f"Beklenmeyen hata (predictWithAI): {e}")
            return AIPredictionResponse(tip="Diğer", olasilik=0.0)

    def getTaskTypes(self) -> List[TaskType]:
        try:
            return self._taskTypeService.getAll()
        except Exception as e:
            logger.error(f"Talep tipleri hatası: {e}")
            return []

    def addTaskType(self, req: AddTaskTypeRequest) -> bool:
        try:
            isim = self._assembler.toAddTaskTypeData(req)
            return self._taskTypeService.add(isim)
        except ValueError as e:
            logger.error(f"Talep tipi ekleme hatası: {e}")
            return False
        except Exception as e:
            logger.error(f"Beklenmeyen hata (addTaskType): {e}")
            return False

    def deleteTaskType(self, isim: str) -> bool:
        try:
            return self._taskTypeService.delete(isim)
        except ValueError as e:
            logger.error(f"Talep tipi silme hatası: {e}")
            return False
        except Exception as e:
            logger.error(f"Beklenmeyen hata (deleteTaskType): {e}")
            return False
