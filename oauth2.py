from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt_token
from database import SessionDep
from sqlmodel import select
import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(session: SessionDep,data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = jwt_token.verify_token(data, credentials_exception)
    user = session.exec(select(models.User).where(models.User.email == token_data.username)).first()
    if not user:
        raise credentials_exception
    return user
