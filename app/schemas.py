# schemas.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

#########################################################################
##### Uses pydantic for cache/dynamic objects; not referenced in DB #####
#########################################################################

#Base JWT AuthToken model
class AuthToken(BaseModel):
    uuid: str
    username: str
    email: EmailStr
    role: Optional[str] = None
    exp: Optional[int] = None  # Optional expiry (timestamp) for the JWT

    class Config:
        extra = "allow"

class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserReadDTO(BaseModel):
    uuid: str
    username: str
    email: EmailStr

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class ProductCreateDTO(BaseModel):
    name: str
    price: float
    unit: str

class ProductReadDTO(BaseModel):
    product_uuid: str
    name: str
    price: float
    unit: str

class ProductInOrder(BaseModel):
    product_uuid: str
    quantity: int

class OrderCreateDTO(BaseModel):
    items: List[ProductInOrder]

class OrderShortReadDTO(BaseModel):
    uuid: str
    date: datetime
    total: float

class ProductId(BaseModel):
    product_uuid: str

class ProductFull(BaseModel):
    uuid: str
    product: ProductId
    quantity: int
    total: float

class OrderReadDTO(BaseModel):
    uuid: str
    date: datetime
    items: List[ProductFull]
    total: float
