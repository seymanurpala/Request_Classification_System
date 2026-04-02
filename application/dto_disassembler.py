from typing import List

from domain.task.task import Task
from application.dto.response.task_response import TaskResponse
from application.dto.response.ai_prediction_response import AIPredictionResponse

#Domain nesnesinden Response DTO'ya çevirir. 
class TaskDtoDisassembler:

    def toResponse(self, task: Task) -> TaskResponse:
        return TaskResponse(
            id              = task.id,
            talepMetni      = task.talepMetni,
            vatandasAdi     = task.vatandasAdi,
            ilce            = task.ilce,
            gelisKanali     = task.gelisKanali,
            tahminTipi      = task.tahminTipi,
            tahminOlasiligi = task.tahminOlasiligi,
            topKTahminler   = task.topKTahminler or [],
            onaylananTip    = task.onaylananTip,
            onaylandiMi     = task.onaylandiMi,
            olusturmaTarihi = task.olusturmaTarihi,
        )

    def toResponseList(self, tasks: List[Task]) -> List[TaskResponse]:
        return [self.toResponse(t) for t in tasks]

    def toPredictionResponse(self, result: dict) -> AIPredictionResponse:
        return AIPredictionResponse(
            tip      = result["tip"],
            olasilik = result["olasilik"],
            topK     = result.get("top_k", []),
        )
