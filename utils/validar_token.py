
import jwt
from config import SECRET_KEY

def verificar_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data["correo"]
    except:
        return None