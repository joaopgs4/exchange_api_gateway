# schemas.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

#########################################################################
##### Uses pydantic for cache/dynamic objects; not referenced in DB #####
#########################################################################

#Base JWT AuthToken model
class AuthToken(BaseModel):
    id : int
    username : str
    email : str
    role : Optional[str] = None
    exp : Optional[int] = None  # Optional expiry (timestamp) for the JWT

    # Allow any additional fields
    class Config:
        extra = "allow"

class UserCreateDTO(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserReadDTO(BaseModel):
    id : int
    username : str
    email : EmailStr

class UserLoginDTO(BaseModel):
    email : EmailStr
    password : str

class ProductCreateDTO(BaseModel):
    name : str
    price : float
    unit : str

class ProductReadDTO(BaseModel):
    id : int
    name : str
    price : float
    unit : str

class ProductInOrder(BaseModel):
    id : int
    quantity : int

class OrderCreateDTO(BaseModel):
    items : List[ProductInOrder]

class OrderShortReadDTO(BaseModel):
    id : int
    date : datetime
    total : float

class ProductId(BaseModel):
    id : int

class ProductFull(BaseModel):
    id : int
    product : ProductId
    quantity : int
    total : float


class OrderReadDTO(BaseModel):
    id : int
    date : datetime
    items : List[ProductFull]
    total : float