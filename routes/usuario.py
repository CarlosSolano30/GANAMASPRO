from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from utils.validar_token import validar_token
import os
from bson import ObjectId

bp_usuario = Blueprint('usuario', __name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.ganaplus
usuarios = db.usuarios

@bp_usuario.route("/api/usuario/perfil", methods=["GET"])
@validar_token
def obtener_perfil(usuario_actual):
    usuario = usuarios.find_one({"correo": usuario_actual["correo"]})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "saldo": usuario.get("saldo", 0),
        "tareas_completadas": usuario.get("tareas_completadas", 0),
        "referidos": usuario.get("referidos", [])
    })
