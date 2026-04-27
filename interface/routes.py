import os

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from application.dto.request.add_task_type_request import AddTaskTypeRequest
from application.dto.request.ai_prediction_request import AIPredictionRequest
from application.dto.request.approve_task_request import ApproveTaskRequest
from application.dto.request.create_task_request import CreateTaskRequest

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
bp = Blueprint("task", __name__, template_folder=_TEMPLATE_DIR)
_app = None


def initRoutes(app):
    global _app
    _app = app


@bp.route("/")
def index():
    return render_template(
        "pages/task_list.html",
        tasks=_app.listTasks(),
        taskTypes=_app.getTaskTypes(),
    )


@bp.route("/task/new")
def newTaskForm():
    return render_template(
        "pages/task_new.html",
        taskTypes=_app.getTaskTypes(),
        channels=_app.getChannels(),
    )


@bp.route("/task/save", methods=["POST"])
def saveTask():
    req = CreateTaskRequest(
        talepMetni=request.form.get("talep_metni"),
        vatandasAdi=request.form.get("vatandas_adi"),
        ilce=request.form.get("ilce"),
        gelisKanali=request.form.get("gelis_kanali"),
        talepTipi=request.form.get("talep_tipi") or None,
    )
    success = _app.createTask(req)
    if success:
        flash("Talep başarıyla kaydedildi.", "success")
    else:
        flash("Talep kaydedilemedi. L\u00fctfen bilgileri kontrol ediniz.", "danger")
    return redirect(url_for("task.index"))


@bp.route("/task/approve/<task_id>", methods=["POST"])
def approveTask(task_id):
    onaylananTip = request.form.get("onaylanan_tip")
    if onaylananTip:
        success = _app.approveTask(ApproveTaskRequest(taskId=task_id, onaylananTip=onaylananTip))
        if success:
            flash("Talep onayland\u0131.", "success")
        else:
            flash("Talep onaylanamad\u0131.", "danger")
    else:
        flash("Onaylanacak tip se\u00e7ilmedi.", "danger")
    return redirect(url_for("task.index"))


@bp.route("/predict")
def predict():
    result = _app.predictWithAI(AIPredictionRequest(metin=request.args.get("text", "")))
    return jsonify({"tahmin": result.tip, "olasilik": result.olasilik, "top_k": result.topK})


@bp.route("/task-type/settings")
def taskTypeSettings():
    return render_template("pages/task_type.html", taskTypes=_app.getTaskTypesForSettings())


@bp.route("/task-type/add", methods=["POST"])
def addTaskType():
    isim = request.form.get("isim")
    if isim:
        success = _app.addTaskType(AddTaskTypeRequest(isim=isim))
        if success:
            flash("Talep tipi eklendi. Formlarda g\u00f6r\u00fcnmesi i\u00e7in modeli yeniden e\u011fitmelisiniz.", "info")
        else:
            flash("Bu tip zaten mevcut veya eklenemedi.", "warning")
    else:
        flash("Talep tipi bo\u015f olamaz.", "warning")
    return redirect(url_for("task.taskTypeSettings"))


@bp.route("/task-type/delete/<string:isim>", methods=["POST"])
def deleteTaskType(isim):
    success = _app.deleteTaskType(isim)
    if success:
        flash("Tip silindi.", "success")
    else:
        flash("Tip silinemedi.", "danger")
    return redirect(url_for("task.taskTypeSettings"))
