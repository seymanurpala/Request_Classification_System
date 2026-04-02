from application.dto.request.create_task_request import CreateTaskRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.add_task_type_request import AddTaskTypeRequest

#Request DTO'dan domain'e veri taşır. 
class TaskDtoAssembler:

    def toCreateData(self, req: CreateTaskRequest) -> dict:
        return {
            "talepMetni":  req.talepMetni,
            "vatandasAdi": req.vatandasAdi,
            "ilce":        req.ilce,
            "gelisKanali": req.gelisKanali,
            "talepTipi":   req.talepTipi,
        }

    def toApproveData(self, req: ApproveTaskRequest) -> tuple:
        return req.taskId, req.onaylananTip

    def toAddTaskTypeData(self, req: AddTaskTypeRequest) -> str:
        return req.isim
