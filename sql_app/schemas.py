from typing import Optional

from pydantic import BaseModel


class TypeBase(BaseModel):
    name: str

class Type(TypeBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str
    first_name: str
    last_name: str
    types: list[Type] = []


class UserCreate(UserBase):
    password: str




class TypeCreate(TypeBase):
    pass

class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


