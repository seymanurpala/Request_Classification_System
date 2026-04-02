class TaskType:
    def __init__(self, value: str):
        self.value = value.strip()

    def __str__(self):
        return self.value
