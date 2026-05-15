from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AIPredictionResponse:
    tip:      Optional[str]
    olasilik: float
    topK:     List[dict] = field(default_factory=list)
