

from functools import wraps
from flask import request, jsonify
import jwt
import os
from config import SECRET_KEY

def validar_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token faltante"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return f(usuario_actual=data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

    return decorated_function
