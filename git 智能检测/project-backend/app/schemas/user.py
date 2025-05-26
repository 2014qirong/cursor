from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str 