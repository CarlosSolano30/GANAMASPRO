from flask import Blueprint, jsonify
from utils.validar_token import validar_token

bp_tareas = Blueprint('tareas', __name__)

# Simulación de muros (luego conectamos con AdGate, Monlix, etc.)
@bp_tareas.route("/api/tareas", methods=["GET"])
@validar_token
def listar_tareas(usuario_actual):
    tareas = [
        {"id": 1, "nombre": "Completa una encuesta", "monto": 800},
        {"id": 2, "nombre": "Descarga una app", "monto": 1200},
        {"id": 3, "nombre": "Registrarse en una web", "monto": 1000}
    ]
    return jsonify({"tareas": tareas})
