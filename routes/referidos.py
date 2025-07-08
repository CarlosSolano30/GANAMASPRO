from flask import Blueprint, request, jsonify, current_app
from utils.validar_token import verificar_token

bp = Blueprint("referidos", __name__)

@bp.route("/", methods=["GET"])
def obtener_referidos():
    db = current_app.config["DB"]
    token = request.headers.get("Authorization")
    correo = verificar_token(token)

    if not correo:
        return jsonify({"error": "Token inválido"}), 401

    usuario = db.usuarios.find_one({"correo": correo})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "referidos": usuario.get("referidos", []),
        "ganancia_referidos": usuario.get("saldo", 0)
    })