from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str

class UserInDB(User):
    password: str

class RegisterInput(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class EvaluationResult(BaseModel):
    user_id: UUID
    score: float
    passed: bool