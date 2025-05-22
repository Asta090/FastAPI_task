from fastapi import APIRouter, HTTPException, status, Depends
import schemas
import models
import jwt_token
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionDep
from hashing import Hash
from sqlmodel import select



router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(session: SessionDep,request: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(models.User).where(models.User.email == request.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    access_token = jwt_token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}