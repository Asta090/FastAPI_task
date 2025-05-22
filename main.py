from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from models import Order, User
from routes import order, user, auth


app= FastAPI()
app.include_router(auth.router)
app.include_router(order.router)
app.include_router(user.router)




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()