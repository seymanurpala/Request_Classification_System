import re
import pickle
import numpy as np
from tensorflow import keras

from domain.task.i_prediction_service import IPredictionService
import config


class ANNClassifier(IPredictionService):

    def __init__(self):
        self._model      = None
        self._vectorizer = None
        self._encoder    = None
        self._load()

    def _load(self) -> None:
        self._model = keras.models.load_model(config.MODEL_PATH)
        with open(config.VECTORIZER_PATH, "rb") as f:
            self._vectorizer = pickle.load(f)
        with open(config.ENCODER_PATH, "rb") as f:
            self._encoder = pickle.load(f)

    def predict(self, metin: str) -> dict:
        if not metin or not metin.strip():
            raise ValueError("Tahmin için metin boş olamaz.")
        temiz      = re.sub(r"[^\w\s]", " ", metin.lower().strip())
        X          = self._vectorizer.transform([temiz]).toarray()
        prob       = self._model.predict(X, verbose=0)[0]
        bestIdx    = int(np.argmax(prob))
        topIndices = np.argsort(prob)[::-1][:config.TOP_K]
        return {
            "tip":      str(self._encoder.classes_[bestIdx]),
            "olasilik": float(prob[bestIdx]),
            "top_k":    [
                {"tip": str(self._encoder.classes_[i]), "olasilik": round(float(prob[i]), 4)}
                for i in topIndices
            ],
        }
