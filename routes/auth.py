from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from config import SECRET_KEY
from models.usuario import crear_usuario, buscar_por_correo

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    db = current_app.config["DB"]
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    telefono = data.get("telefono")
    password = generate_password_hash(data.get("password"))
    referido = data.get("referido")

    if buscar_por_correo(db, correo):
        return jsonify({"error": "Este correo ya está registrado"}), 400

    nuevo_usuario = crear_usuario({
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "password": password,
        "referido": referido,
        "fecha_registro": datetime.datetime.utcnow()
    })
    db.usuarios.insert_one(nuevo_usuario)
    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

@bp.route("/login", methods=["POST"])
def login():
    db = current_app.config["DB"]
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("password")

    usuario = buscar_por_correo(db, correo)
    if not usuario or not check_password_hash(usuario["password"], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = jwt.encode({
        "correo": usuario["correo"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "es_admin": usuario["es_admin"]})