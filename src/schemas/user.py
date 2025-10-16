from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime, timezone

class User(BaseModel):
    id: int = Field(description="Id юзера")
    email: EmailStr = Field(description="Email юзера")
    role: str = Field(default="user", description="Role юзера")
    is_active: bool = Field(default=True, description="Статус пользователя")
    date_joined: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email")
    password: str = Field(min_length=8, description="Password, минимальный размер пороля 8")