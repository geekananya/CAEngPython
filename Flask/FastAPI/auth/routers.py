from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .auth import register_user, authenticate_user
from .security import create_access_token, oauth2_scheme, get_user
from FastAPI.database import get_db       # python doesn't record where a package was loaded from. So relative imports wont work
from FastAPI.schemas import User

router = APIRouter()

@router.post('/register')
async def register(user: User, db: Session = Depends(get_db)):            # dependency injection by fastapi
    return register_user(user, db)


@router.post("/token")
async def login_and_send_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/logout')
async def logout(Authorization: str = Header(None), db: Session = Depends(get_db)):
    user = get_user(db)
    try:
        oauth2_scheme.revoke_token(Authorization)
    except Exception as e:
        print(e)
        return {}
    return {"logged out": user}
