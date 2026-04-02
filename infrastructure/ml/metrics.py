import numpy as np
from sklearn.metrics import f1_score, confusion_matrix, classification_report


def topKAccuracy(yTrue: list, yProb: np.ndarray, k: int = 3) -> float:
    topKIdx = np.argsort(yProb, axis=1)[:, -k:]
    correct = sum(gt in pred for gt, pred in zip(yTrue, topKIdx))
    return correct / len(yTrue)


def bootstrapF1(yTrue: list, yPred: list, n: int = 1000, ci: float = 0.95) -> dict:
    rng    = np.random.default_rng(42)
    scores = [
        f1_score(
            np.array(yTrue)[idx := rng.integers(0, len(yTrue), size=len(yTrue))],
            np.array(yPred)[idx],
            average="macro", zero_division=0
        )
        for _ in range(n)
    ]
    arr = np.array(scores)
    return {
        "mean":  arr.mean(),
        "std":   arr.std(),
        "lower": np.percentile(arr, (1 - ci) / 2 * 100),
        "upper": np.percentile(arr, (1 - (1 - ci) / 2) * 100),
    }


def calculateMetrics(yTrue: list, yPred: list, classes: list) -> dict:
    yProb = np.eye(len(classes))[[classes.index(x) for x in yPred]]
    return {
        "macroF1":         f1_score(yTrue, yPred, average="macro",    zero_division=0),
        "weightedF1":      f1_score(yTrue, yPred, average="weighted", zero_division=0),
        "topKAccuracy":    topKAccuracy([classes.index(x) for x in yTrue], yProb),
        "topK":            3,
        "bootstrap":       bootstrapF1(yTrue, yPred),
        "confusionMatrix": confusion_matrix(yTrue, yPred),
        "report":          classification_report(yTrue, yPred, target_names=classes, output_dict=True, zero_division=0),
        "classes":         classes,
    }
