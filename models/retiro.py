import datetime
from bson.objectid import ObjectId

def crear_retiro(data, correo_usuario, neto):
    return {
        "correo_usuario": correo_usuario,
        "metodo": data.get("metodo"),
        "cuenta": data.get("cuenta"),
        "monto_solicitado": int(data.get("monto")),
        "monto_neto": neto,
        "estado": "pendiente",
        "fecha": datetime.datetime.utcnow()
    }

def aprobar_retiro(db, retiro_id):
    db.retiros.update_one(
        {"_id": ObjectId(retiro_id)},
        {"$set": {"estado": "pagado"}}
    )