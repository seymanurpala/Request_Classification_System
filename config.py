import os

MONGO_URI        = "mongodb://localhost:27017"
MONGO_DB         = "talep_db"
MONGO_COLLECTION = "talepler"

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH      = os.path.join(BASE_DIR, "infrastructure", "saved_model", "ann_model.keras")
ENCODER_PATH    = os.path.join(BASE_DIR, "infrastructure", "saved_model", "label_encoder.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "infrastructure", "saved_model", "tfidf_vectorizer.pkl")

LIST_LIMIT   = 50
TEST_SIZE    = 0.2
RANDOM_STATE = 42
EPOCHS       = 30
BATCH_SIZE   = 32
TOP_K        = 3

SECRET_KEY  = "talep-siniflandirma-secret"
FLASK_DEBUG = True
FLASK_PORT  = 5000
