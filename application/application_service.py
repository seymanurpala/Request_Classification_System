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

import config

logger = logging.getLogger(__name__)


class AppService:

    def __init__(
        self,
        taskService:       TaskService,
        taskTypeService:   TaskTypeService,
        predictionService: IPredictionService,
    ):
        self._taskService       = taskService
        self._taskTypeService   = taskTypeService
        self._predictionService = predictionService
        self._assembler         = TaskDtoAssembler()
        self._disassembler      = TaskDtoDisassembler()

    def createTask(self, req: CreateTaskRequest) -> bool:
        try:
            data       = self._assembler.toCreateData(req)
            prediction = self._predictionService.predict(data["talepMetni"])

            self._taskService.save(
                talepMetni      = data["talepMetni"],
                vatandasAdi     = data["vatandasAdi"],
                ilce            = data["ilce"],
                gelisKanali     = data["gelisKanali"],
                talepTipi       = prediction["tip"],
                tahminOlasiligi = prediction["olasilik"],
                topKTahminler   = prediction["top_k"],
            )
            return True
        except ValueError as e:
            logger.error(f"Talep oluşturma hatası: {e}")
            return False
        except Exception as e:
            logger.error(f"Beklenmeyen hata (createTask): {e}")
            return False

    def listTasks(self, limit: int = config.LIST_LIMIT) -> List[TaskResponse]:
        try:
            tasks = self._taskService.getAll(limit)
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