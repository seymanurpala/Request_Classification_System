from dataclasses import dataclass


@dataclass
class TaskType:
    value: str

    def __post_init__(self) -> None:
        self.value = self.value.strip()

    def __str__(self) -> str:
        return self.value
