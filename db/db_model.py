from pydantic import BaseModel
from typing import Optional

class Fruit(BaseModel):
  
    name: str
    price: int
    quantity: int



class Student(BaseModel):
    name: str
    subject: list[str]
    age: int
    grade: Optional[str] = None



class pfp(BaseModel):
    photo:str
    name:str


class User(BaseModel):
    username: str
    email: str
    password: str

class userout(BaseModel):
    username: str
    email: str

class Userlogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str




