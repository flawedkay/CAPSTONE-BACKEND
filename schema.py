from pydantic import BaseModel
from typing import Optional
from fastapi import Request


class SignupDetails(BaseModel):
    email: str
    username: str
    firstname: str
    lastname: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


