import jwt
from datetime import datetime, timedelta, timezone
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from FastAPI.models import User as DbUser

SECRET_KEY = "f0917ba04c0d74a1026d3d55314451357ae8a8f716022cada288e2354a95cba1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None =None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password):
    return password_context.hash(password)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


# util fn -- validate token associated with req
def get_user(db, token: str = Depends(oauth2_scheme)):              # oauth2 helps to extract the token from the request.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    # to get db instance either pass it as param or use dependency injection to get_db by importing get_db everywhere.
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if user is None:
        raise credentials_exception
    return user