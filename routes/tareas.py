from flask import Blueprint, request, jsonify, current_app
from utils.validar_token import verificar_token
from models.usuario import buscar_por_correo, actualizar_saldo_y_tareas, sumar_bono_a_referido

bp = Blueprint("tareas", __name__)

@bp.route("/completar", methods=["POST"])
def completar_tarea():
    db = current_app.config["DB"]
    token = request.headers.get("Authorization")
    correo = verificar_token(token)

    if not correo:
        return jsonify({"error": "Token inválido o ausente"}), 401

    usuario = buscar_por_correo(db, correo)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    nuevas_tareas = usuario.get("tareas_completadas", 0) + 1
    nuevo_saldo = usuario.get("saldo", 0) + 1000

    actualizar_saldo_y_tareas(db, correo, nuevo_saldo, nuevas_tareas)

    if usuario.get("referido_por") and nuevas_tareas in [3, 7, 15]:
        bono = {3: 3000, 7: 5000, 15: 7000}[nuevas_tareas]
        sumar_bono_a_referido(db, usuario["referido_por"], correo, bono)

    return jsonify({"mensaje": "Tarea completada", "tareas_completadas": nuevas_tareas, "saldo": nuevo_saldo})