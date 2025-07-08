from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URI
import routes.auth as auth_routes
import routes.tareas as tareas_routes
import routes.referidos as referidos_routes
import routes.retiros as retiros_routes
import routes.admin as admin_routes

app = Flask(__name__)
CORS(app)

# Conexión a Mongo
client = MongoClient(MONGO_URI)
db = client.ganaplus

# Inyectamos db en cada blueprint
app.register_blueprint(auth_routes.bp, url_prefix="/api/auth")
app.register_blueprint(tareas_routes.bp, url_prefix="/api/tareas")
app.register_blueprint(referidos_routes.bp, url_prefix="/api/referidos")
app.register_blueprint(retiros_routes.bp, url_prefix="/api/retiros")
app.register_blueprint(admin_routes.bp, url_prefix="/api/admin")

if __name__ == "__main__":
    app.run(debug=True)
