from flask import Blueprint, jsonify, request

from application.dto.request.add_task_type_request import AddTaskTypeRequest
from application.dto.request.ai_prediction_request import AIPredictionRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.create_task_request import CreateTaskRequest

bp = Blueprint("task", __name__)
_app = None


def initRoutes(app):
    global _app
    _app = app


@bp.route("/api/tasks")
def getTasks():
    tasks = _app.listTasks()
    taskTypes = _app.getTaskTypes()
    return jsonify({
        "tasks": [t.__dict__ for t in tasks],
        "taskTypes": [tt.__dict__ for tt in taskTypes],
    })


@bp.route("/api/task/new")
def getNewTaskFormData():
    return jsonify({
        "taskTypes": [tt.__dict__ for tt in _app.getTaskTypes()],
        "channels": _app.getChannels(),
    })


@bp.route("/api/task/save", methods=["POST"])
def saveTask():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Geçersiz JSON verisi."}), 400

    req = CreateTaskRequest(
        talepMetni=data.get("talep_metni"),
        vatandasAdi=data.get("vatandas_adi"),
        ilce=data.get("ilce"),
        gelisKanali=data.get("gelis_kanali"),
        talepTipi=data.get("talep_tipi") or None,
    )
    success = _app.createTask(req)
    if success:
        return jsonify({"success": True, "message": "Talep başarıyla kaydedildi."})
    return jsonify({"success": False, "message": "Talep kaydedilemedi. Lütfen bilgileri kontrol ediniz."}), 400


@bp.route("/api/task/approve/<task_id>", methods=["POST"])
def approveTask(task_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Geçersiz JSON verisi."}), 400

    onaylananTip = data.get("onaylanan_tip")
    if not onaylananTip:
        return jsonify({"success": False, "message": "Onaylanacak tip seçilmedi."}), 400
    success = _app.approveTask(ApproveTaskRequest(taskId=task_id, onaylananTip=onaylananTip))
    if success:
        return jsonify({"success": True, "message": "Talep onaylandı."})
    return jsonify({"success": False, "message": "Talep onaylanamadı."}), 400


@bp.route("/api/predict")
def predict():
    result = _app.predictWithAI(AIPredictionRequest(metin=request.args.get("text", "")))
    return jsonify({"tahmin": result.tip, "olasilik": result.olasilik, "top_k": result.topK})


@bp.route("/api/task-types")
def getTaskTypes():
    return jsonify({
        "taskTypes": [tt.__dict__ for tt in _app.getTaskTypesForSettings()],
    })


@bp.route("/api/task-type/add", methods=["POST"])
def addTaskType():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Geçersiz JSON verisi."}), 400

    isim = data.get("isim")
    if not isim:
        return jsonify({"success": False, "message": "Talep tipi boş olamaz."}), 400
    success = _app.addTaskType(AddTaskTypeRequest(isim=isim))
    if success:
        return jsonify({"success": True, "message": "Talep tipi eklendi. Formlarda görünmesi için modeli yeniden eğitmelisiniz."})
    return jsonify({"success": False, "message": "Bu tip zaten mevcut veya eklenemedi."}), 400


@bp.route("/api/task-type/delete/<string:isim>", methods=["DELETE"])
def deleteTaskType(isim):
    success = _app.deleteTaskType(isim)
    if success:
        return jsonify({"success": True, "message": "Tip silindi."})
    return jsonify({"success": False, "message": "Tip silinemedi."}), 400
