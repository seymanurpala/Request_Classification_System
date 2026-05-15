from abc import ABC, abstractmethod


class IPredictionService(ABC):

    @abstractmethod
    def predict(self, metin: str) -> dict: ...

    @abstractmethod
    def getSupportedTypes(self) -> set[str]: ...
