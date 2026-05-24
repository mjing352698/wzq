from jose import JWTError,jwt
from datetime import datetime,timedelta
SECRET_KEY = '123456'
ALGORITHM = 'HS256'
def generate_token(username):
    payload = {'sub':username}
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token
def check_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username = payload.get('sub')
        if username is None:
            raise None
        return username
    except JWTError:
        return None

