from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionDep
import models
import schemas
from hashing import Hash

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post("/register", response_model=schemas.ShowUser)
def create_user(request: schemas.User, session: SessionDep):
    db_user = models.User(
        username=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user