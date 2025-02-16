import jwt
import datetime
from core.config import SECRET_KEY

def create_jwt_token(email: str):
    token = jwt.encode({"sub": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, SECRET_KEY, algorithm="HS256")
    return token