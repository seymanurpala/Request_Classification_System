from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class TaskResponse:
    id:              str
    talepMetni:      str
    vatandasAdi:     str
    ilce:            str
    gelisKanali:     Optional[str]
    tahminTipi:      Optional[str]
    tahminOlasiligi: Optional[float]
    topKTahminler:   List[dict]
    onaylananTip:    Optional[str]
    onaylandiMi:     bool
    olusturmaTarihi: datetime
