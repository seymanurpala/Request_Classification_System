from dataclasses import dataclass, field
from typing import List


@dataclass
class AIPredictionResponse:
    tip:      str
    olasilik: float
    topK:     List[dict] = field(default_factory=list)
