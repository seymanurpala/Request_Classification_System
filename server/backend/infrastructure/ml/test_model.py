import csv
from pathlib import Path
import sys

from sklearn.metrics import accuracy_score, f1_score, classification_report

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from infrastructure.ml.ann_classifier import ANNClassifier

clf = ANNClassifier()

dataset_path = Path(config.BASE_DIR) / "infrastructure" / "data" / "talep_ornek.csv"

with dataset_path.open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

y_true = [r["talepTipi"] for r in rows]
y_pred = [clf.predict(r["talepMetni"])["tip"] for r in rows]

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Macro F1:", f1_score(y_true, y_pred, average="macro"))
print()
print(classification_report(y_true, y_pred, zero_division=0))
