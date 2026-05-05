from dataclasses import dataclass


@dataclass
class TaskType:
    value: str

    def __str__(self) -> str:
        return self.value

