def crear_usuario(data):
    return {
        "nombre": data.get("nombre"),
        "correo": data.get("correo"),
        "telefono": data.get("telefono"),
        "password": data.get("password"),
        "saldo": 0,
        "tareas_completadas": 0,
        "referidos": [],
        "es_admin": False,
        "referido_por": data.get("referido") or None,
        "fecha_registro": data.get("fecha_registro")
    }

def buscar_por_correo(db, correo):
    return db.usuarios.find_one({"correo": correo})

def actualizar_saldo_y_tareas(db, correo, saldo, tareas):
    db.usuarios.update_one(
        {"correo": correo},
        {"$set": {"saldo": saldo, "tareas_completadas": tareas}}
    )

def sumar_bono_a_referido(db, correo_referido, correo_hijo, bono):
    db.usuarios.update_one(
        {"correo": correo_referido},
        {"$inc": {"saldo": bono}, "$push": {"referidos": correo_hijo}}
    )
