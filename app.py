import os
from flask import Flask
from interface.routes import bp as taskBp, initRoutes

from application.application_service import AppService
from domain.task.task_service import TaskService
from domain.task.task_repository import TaskRepository
from domain.task_type.task_type_service import TaskTypeService
from domain.task_type.task_type_repository import TaskTypeRepository
from infrastructure.ml.ann_classifier import ANNClassifier

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def createApp() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(_BASE_DIR, "config.py"))

    appService = AppService(
        taskService       = TaskService(TaskRepository()),
        taskTypeService   = TaskTypeService(TaskTypeRepository()),
        predictionService = ANNClassifier(),
    )

    initRoutes(appService)
    app.register_blueprint(taskBp)

    return app


if __name__ == "__main__":
    createApp().run(debug=True, port=5000)