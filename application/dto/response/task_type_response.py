from dataclasses import dataclass


@dataclass
class TaskTypeResponse:
    value: str
    supported: bool = True
