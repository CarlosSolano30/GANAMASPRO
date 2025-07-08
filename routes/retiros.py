from flask import Blueprint, request, jsonify, current_app
from utils.validar_token import verificar_token
from models.usuario import buscar_por_correo
from models.retiro import crear_retiro

bp = Blueprint("retiros", __name__)

@bp.route("/solicitar", methods=["POST"])
def solicitar_retiro():
    db = current_app.config["DB"]
    token = request.headers.get("Authorization")
    correo = verificar_token(token)

    if not correo:
        return jsonify({"error": "Token inválido"}), 401

    data = request.get_json()
    metodo = data.get("metodo")
    cuenta = data.get("cuenta")
    monto = int(data.get("monto"))

    usuario = buscar_por_correo(db, correo)
    if monto < 25000 or usuario["saldo"] < monto:
        return jsonify({"error": "Monto inválido o saldo insuficiente"}), 400

    neto = int(monto * 0.9)
    retiro = crear_retiro(data, correo, neto)
    db.retiros.insert_one(retiro)
    db.usuarios.update_one({"correo": correo}, {"$set": {"saldo": usuario["saldo"] - monto}})

    return jsonify({"mensaje": "Retiro solicitado", "monto_neto": neto})
