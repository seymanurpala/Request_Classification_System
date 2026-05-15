from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from infrastructure.data.dataset_uret import SABLONLAR
from infrastructure.persistence.mongo_client import getDb


def sync_task_types():
    task_types = list(SABLONLAR.keys())
    col = getDb()[config.TASK_TYPE_COLLECTION]

    col.delete_many({})
    col.insert_many([{"isim": name} for name in task_types])

    print("Talep tipleri senkronize edildi.")
    print("Toplam tip sayısı:", len(task_types))
    for name in task_types:
        print(name)


if __name__ == "__main__":
    sync_task_types()
