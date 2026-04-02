from domain.task_type.types import TaskType


class TaskTypeFactory:

    @staticmethod
    def create(isim: str) -> TaskType:
        return TaskType(isim)
