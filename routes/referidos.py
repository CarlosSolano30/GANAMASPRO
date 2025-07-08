from flask import Blueprint, jsonify
from pymongo import MongoClient
from utils.validar_token import validar_token
import os

bp_referidos = Blueprint('referidos', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.ganaplus
usuarios = db.usuarios

@bp_referidos.route("/api/referidos", methods=["GET"])
@validar_token
def obtener_referidos(usuario_actual):
    user = usuarios.find_one({"correo": usuario_actual["correo"]})
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    referidos = usuarios.find({"referido_por": user["correo"]})
    lista = []
    for r in referidos:
        lista.append({
            "nombre": r["nombre"],
            "correo": r["correo"],
            "tareas_completadas": r.get("tareas_completadas", 0)
        })

    return jsonify({"referidos": lista})
