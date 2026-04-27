from application.dto.request.create_task_request import CreateTaskRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.add_task_type_request import AddTaskTypeRequest


# dışarıdan gelen request verisini sistemin içeride kullanacağı hale çevirir.
class TaskDtoDisassembler:

    def toCreateData(self, req: CreateTaskRequest) -> dict:
        return {
            "talepMetni":  (req.talepMetni or "").strip(),
            "vatandasAdi": (req.vatandasAdi or "").strip(),
            "ilce":        (req.ilce or "").strip(),
            "gelisKanali": (req.gelisKanali or "").strip(),
            "manuelTip":   ((req.talepTipi or "").strip() or None),
        }

    def toApproveData(self, req: ApproveTaskRequest) -> dict:
        return {
            "taskId": (req.taskId or "").strip(),
            "onaylananTip": (req.onaylananTip or "").strip(),
        }

    def toAddTaskTypeData(self, req: AddTaskTypeRequest) -> dict:
        return {"isim": (req.isim or "").strip()}
