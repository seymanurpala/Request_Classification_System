import csv
from pathlib import Path
import sys
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from infrastructure.ml.ann_classifier import ANNClassifier, preprocess_text


DATASET_PATH = Path(config.BASE_DIR) / "infrastructure" / "data" / "talep_ornek.csv"


def topKAccuracy(yTrue: list, yProb: np.ndarray, k: int = 3) -> float:
    if len(yTrue) == 0:
        return 0.0
    k = min(k, yProb.shape[1])
    topKIdx = np.argsort(yProb, axis=1)[:, -k:]
    correct = sum(gt in pred for gt, pred in zip(yTrue, topKIdx))
    return correct / len(yTrue)


def bootstrapF1(yTrue: list, yPred: list, n: int = 1000, ci: float = 0.95) -> dict:
    rng = np.random.default_rng(42)
    yTrueArr = np.array(yTrue)
    yPredArr = np.array(yPred)
    scores = []
    for _ in range(n):
        idx = rng.integers(0, len(yTrue), size=len(yTrue))
        scores.append(
            f1_score(
                yTrueArr[idx],
                yPredArr[idx],
                average="macro",
                zero_division=0,
            )
        )
    arr = np.array(scores)
    return {
        "mean":  arr.mean(),
        "std":   arr.std(),
        "lower": np.percentile(arr, (1 - ci) / 2 * 100),
        "upper": np.percentile(arr, (1 - (1 - ci) / 2) * 100),
    }


def calculateMetrics(yTrue: list, yPred: list, classes: list, yProb: np.ndarray) -> dict:
    topK = min(3, len(classes))
    yTrueIdx = [classes.index(x) for x in yTrue]
    return {
        "macroF1":         f1_score(yTrue, yPred, average="macro",    zero_division=0),
        "weightedF1":      f1_score(yTrue, yPred, average="weighted", zero_division=0),
        "topKAccuracy":    topKAccuracy(yTrueIdx, yProb, k=topK),
        "topK":            topK,
        "bootstrap":       bootstrapF1(yTrue, yPred),
        "confusionMatrix": confusion_matrix(yTrue, yPred),
        "report":          classification_report(yTrue, yPred, target_names=classes, output_dict=True, zero_division=0),
        "classes":         classes,
    }


def loadDataset():
    with DATASET_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    texts = [preprocess_text(row["talepMetni"]) for row in rows]
    labels = [row["talepTipi"].strip() for row in rows]
    return texts, labels


def predictDataset(texts: list):
    clf = ANNClassifier()
    X = clf._vectorizer.transform(texts).toarray()
    yProb = clf._model.predict(X, verbose=0)
    classes = [str(x) for x in clf._encoder.classes_]
    yPred = [classes[int(np.argmax(prob))] for prob in yProb]
    return yPred, yProb, classes


def main():
    texts, yTrue = loadDataset()
    yPred, yProb, classes = predictDataset(texts)
    metrics = calculateMetrics(yTrue, yPred, classes, yProb)

    print("Toplam veri sayisi:", len(yTrue))
    print("Sinif sayisi:", len(classes))
    print("Accuracy:", round(accuracy_score(yTrue, yPred), 4))
    print("Macro F1:", round(metrics["macroF1"], 4))
    print("Weighted F1:", round(metrics["weightedF1"], 4))
    print(f"Top-{metrics['topK']} Accuracy:", round(metrics["topKAccuracy"], 4))
    print()
    print("Bootstrap Macro F1:")
    print("Mean:", round(metrics["bootstrap"]["mean"], 4))
    print("Std:", round(metrics["bootstrap"]["std"], 4))
    print("Lower:", round(metrics["bootstrap"]["lower"], 4))
    print("Upper:", round(metrics["bootstrap"]["upper"], 4))
    print()
    print(
        classification_report(
            yTrue,
            yPred,
            target_names=classes,
            zero_division=0,
        )
    )
    print("Confusion Matrix:")
    print(metrics["confusionMatrix"])


if __name__ == "__main__":
    main()
