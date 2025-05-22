from fastapi import  Query
from sqlmodel import Field,SQLModel,Relationship
from typing import List,Optional

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    order_id:Optional[int] = Field(default=None, primary_key=True)
    product:str = Field(index=True)
    quantity:int = Field(index=True)
    address:str = Field(index=True)
    status:str = Field(default="pending")
    buyer_id:Optional[int] = Field(default=None, foreign_key="users.user_id")
    creator:"User"=Relationship(back_populates="orders")


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id:Optional[int] = Field(default=None, primary_key=True)
    username:str = Field(default=None, unique=True)
    email:str = Field(default=None, unique=True)
    password:str = Field(default=None)
    orders:List['Order'] = Relationship(back_populates="creator")


