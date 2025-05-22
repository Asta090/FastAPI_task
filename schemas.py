from pydantic import BaseModel,EmailStr



class order_base(BaseModel):
  product:str
  quantity:int
  address:str

class order_create(order_base):
  class Config:
    orm_mode = True

class OrderOut(order_base):
    order_id: int
    status: str
    buyer_id: int # To show who placed the orde

class order_status_update(BaseModel):
  status: str


class UserBase(BaseModel):
    name: str
    email: EmailStr


# For creating a user
class User(UserBase):
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class ShowUser(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True