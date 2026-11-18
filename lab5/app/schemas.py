from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr

class UserResponse(UserCreate):
    id: int
    class Config:
        from_attributes = True
