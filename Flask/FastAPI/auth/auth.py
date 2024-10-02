from datetime import timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .security import get_password_hash, verify_password, create_access_token
from Flask.FastAPI.schemas import User as PyUser
from Flask.FastAPI.models import User as DbUser



def register_user(user: PyUser, db):
    if db.query(DbUser).filter(DbUser.username == user.username).first() :
        raise HTTPException(status_code=400, detail="Username already registered")              # add custom exception
    print(user.username)
    new_user = DbUser(
        username=user.username,
        hashed_password = get_password_hash(user.password)
    )
    db.add(new_user)
    # generate token and sign in
    access_token = create_access_token(data={"sub": user.username})
    return {"user": user, "access_token": access_token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if (user is None) or (not verify_password(password, user.hashed_password)):
        return False
    return user
