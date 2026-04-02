from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateTaskRequest:
    talepMetni:  str
    vatandasAdi: str
    ilce:        str
    gelisKanali: str
    talepTipi:   Optional[str] = None
