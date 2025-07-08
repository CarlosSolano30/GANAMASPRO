from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from utils.validar_token import validar_token
import os
import datetime

bp_retiros = Blueprint('retiros', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.ganaplus
usuarios = db.usuarios
retiros = db.retiros

@bp_retiros.route("/api/retiro", methods=["POST"])
@validar_token
def solicitar_retiro(usuario_actual):
    data = request.get_json()
    metodo = data.get("metodo")  # PayPal o Nequi
    destino = data.get("destino")  # número o correo
    monto = data.get("monto")

    if monto < 25000:
        return jsonify({"error": "El monto mínimo es $25,000"}), 400

    descuento = int(monto * 0.10)
    total = monto - descuento

    user = usuarios.find_one({"correo": usuario_actual["correo"]})

    if user["saldo"] < monto:
        return jsonify({"error": "Saldo insuficiente"}), 400

    usuarios.update_one(
        {"correo": usuario_actual["correo"]},
        {"$inc": {"saldo": -monto}}
    )

    retiros.insert_one({
        "usuario": usuario_actual["correo"],
        "metodo": metodo,
        "destino": destino,
        "monto": monto,
        "recibirá": total,
        "fecha": datetime.datetime.utcnow(),
        "estado": "pendiente"
    })

    return jsonify({"mensaje": "Solicitud de retiro enviada"}), 200
