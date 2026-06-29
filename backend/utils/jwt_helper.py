import datetime
import jwt
from config import Config

def sign_token(payload):
    data = payload.copy()
    data["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=Config.JWT_EXPIRES_IN)
    return jwt.encode(data, Config.JWT_SECRET, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])

