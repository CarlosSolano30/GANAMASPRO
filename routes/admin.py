from flask import Blueprint, request, jsonify, current_app
from models.retiro import aprobar_retiro
from utils.validar_token import verificar_token

bp = Blueprint("admin", __name__)

@bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    db = current_app.config["DB"]
    correo = verificar_token(request.headers.get("Authorization"))
    admin = db.usuarios.find_one({"correo": correo})

    if not admin or not admin.get("es_admin"):
        return jsonify({"error": "No autorizado"}), 403

    usuarios = list(db.usuarios.find({}, {"password": 0}))
    for u in usuarios:
        u["_id"] = str(u["_id"])
    return jsonify(usuarios)

@bp.route("/retiros", methods=["GET"])
def listar_retiros():
    db = current_app.config["DB"]
    correo = verificar_token(request.headers.get("Authorization"))
    admin = db.usuarios.find_one({"correo": correo})

    if not admin or not admin.get("es_admin"):
        return jsonify({"error": "No autorizado"}), 403

    retiros = list(db.retiros.find())
    for r in retiros:
        r["_id"] = str(r["_id"])
    return jsonify(retiros)

@bp.route("/retiros/aprobar", methods=["POST"])
def aprobar():
    db = current_app.config["DB"]
    correo = verificar_token(request.headers.get("Authorization"))
    admin = db.usuarios.find_one({"correo": correo})
    if not admin or not admin.get("es_admin"):
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()
    aprobar_retiro(db, data.get("id"))
    return jsonify({"mensaje": "Retiro aprobado"})
