from application.dto.request.create_task_request import CreateTaskRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.add_task_type_request import AddTaskTypeRequest


# dışarıdan gelen request verisini sistemin içeride kullanacağı hale çevirir.
class TaskDtoDisassembler:

    def _cleanText(self,value:str)->str:
        return (value or "").strip()

    def toCreateData(self, req: CreateTaskRequest) -> dict:
        return {
            "talepMetni":  self._cleanText(req.talepMetni),
            "vatandasAdi": self._cleanText(req.vatandasAdi),
            "ilce":        self._cleanText(req.ilce),
            "gelisKanali": self._cleanText(req.gelisKanali),
            "manuelTip":   self._cleanText(req.talepTipi) or None,
        }

    def toApproveData(self, req: ApproveTaskRequest) -> dict:
        return {
            "taskId": self._cleanText(req.taskId),
            "onaylananTip":self._cleanText(req.onaylananTip),
        }

    def toAddTaskTypeData(self, req: AddTaskTypeRequest) -> dict:
        return {"isim":self._cleanText(req.isim)}

    def toDeleteTaskTypeData(self, isim: str) -> dict:
        return {"isim":self._cleanText(isim)}
