from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class AuthRequest(BaseModel):
    email: str
    password: str