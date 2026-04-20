import csv
from pathlib import Path
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from infrastructure.ml.ann_classifier import preprocess_text


DATASET_PATH = Path(config.BASE_DIR) / "infrastructure" / "data" / "talep_ornek.csv"


def load_dataset():
    with DATASET_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    texts = [preprocess_text(row["talepMetni"]) for row in rows]
    labels = [row["talepTipi"].strip() for row in rows]
    return texts, labels


def build_model(input_dim: int, output_dim: int) -> keras.Model:
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(input_dim,)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dropout(0.1),
            keras.layers.Dense(output_dim, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    texts, labels = load_dataset()

    X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(
        texts,
        labels,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=labels,
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_train = vectorizer.fit_transform(X_train_text).toarray().astype(np.float32)
    X_test = vectorizer.transform(X_test_text).toarray().astype(np.float32)

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train_text)
    y_test = encoder.transform(y_test_text)

    model = build_model(X_train.shape[1], len(encoder.classes_))
    model.fit(
        X_train,
        y_train,
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE,
        verbose=0,
    )

    y_prob = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_prob, axis=1)

    print("Toplam veri sayisi:", len(texts))
    print("Train veri sayisi:", len(X_train_text))
    print("Test veri sayisi:", len(X_test_text))
    print("Test Accuracy:", accuracy_score(y_test, y_pred))
    print("Test Macro F1:", f1_score(y_test, y_pred, average="macro"))
    print()
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=encoder.classes_,
            zero_division=0,
        )
    )


if __name__ == "__main__":
    main()
