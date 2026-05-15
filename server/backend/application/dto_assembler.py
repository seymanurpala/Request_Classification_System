from typing import List, Optional

from domain.task.task import Task
from domain.task_type.types import TaskType
from application.dto.response.task_response import TaskResponse
from application.dto.response.ai_prediction_response import AIPredictionResponse
from application.dto.response.task_type_response import TaskTypeResponse


# sistem içindeki veriyi dışarı verilecek response'a çevirir
class TaskDtoAssembler:

    def toResponse(self, task: Task) -> TaskResponse:
        return TaskResponse(
            id              = task.id,
            talepMetni      = task.talepMetni,
            vatandasAdi     = task.vatandasAdi,
            ilce            = task.ilce,
            gelisKanali     = task.gelisKanali,
            manuelTip       = task.manuelTip,
            tahminTipi      = task.tahminTipi,
            tahminOlasiligi = task.tahminOlasiligi,
            topKTahminler   = task.topKTahminler,
            onaylananTip    = task.onaylananTip,
            onaylandiMi     = task.onaylandiMi,
            olusturmaTarihi = task.olusturmaTarihi,
        )

    def toResponseList(self, tasks: List[Task]) -> List[TaskResponse]:
        return [self.toResponse(task) for task in tasks]

    def toPredictionResponse(self, result: dict) -> AIPredictionResponse:
        return AIPredictionResponse(
            tip      = result["tip"],
            olasilik = result["olasilik"],
            topK     = result["top_k"],
        )

    def toTaskTypeResponse(self, taskType: TaskType, supported: bool = True) -> TaskTypeResponse:
        return TaskTypeResponse(value=taskType.value, supported=supported)

    def toTaskTypeResponseList(
        self,
        taskTypes: List[TaskType],
        supportedTypeNames: Optional[set[str]] = None,
    ) -> List[TaskTypeResponse]:
        if supportedTypeNames is None:
            return [self.toTaskTypeResponse(taskType) for taskType in taskTypes]

        return [
            self.toTaskTypeResponse(taskType, supported=(taskType.value in supportedTypeNames))
            for taskType in taskTypes
        ]
