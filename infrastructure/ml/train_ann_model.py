import csv
import pickle
from pathlib import Path
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from infrastructure.ml.ann_classifier import preprocess_text


DATA_PATH = Path(config.BASE_DIR) / "infrastructure" / "data" / "talep_ornek.csv"


def load_dataset():
    with DATA_PATH.open(encoding="utf-8") as f:
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


def train_and_save():
    texts, labels = load_dataset()

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X = vectorizer.fit_transform(texts).toarray().astype(np.float32)

    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    model = build_model(X.shape[1], len(encoder.classes_))
    model.fit(
        X,
        y,
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE,
        verbose=0,
    )

    model.save(config.MODEL_PATH)
    with open(config.VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(config.ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)

    preds = np.argmax(model.predict(X, verbose=0), axis=1)
    accuracy = float(np.mean(preds == y))

    print("Model yeniden egitildi.")
    print("Veri dosyasi:", DATA_PATH)
    print("Sinif sayisi:", len(encoder.classes_))
    print("Siniflar:", list(encoder.classes_))
    print("Egitim verisi accuracy:", round(accuracy, 4))


if __name__ == "__main__":
    train_and_save()
