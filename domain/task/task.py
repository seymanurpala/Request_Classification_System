from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List


@dataclass
class Task:
    talepMetni:       str
    vatandasAdi:      str
    ilce:             str
    gelisKanali:      Optional[str]   = None
    tahminTipi:       Optional[str]   = None
    tahminOlasiligi:  Optional[float] = None
    topKTahminler:    List[dict]      = field(default_factory=list)
    onaylananTip:     Optional[str]   = None
    onaylandiMi:      bool            = False
    olusturmaTarihi:  datetime        = field(default_factory=lambda: datetime.now(timezone.utc))
    guncellemeTarihi: Optional[datetime] = None
    id:               Optional[str]  = None
