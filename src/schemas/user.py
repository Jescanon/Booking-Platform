from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime, timezone

class User(BaseModel):
    id: Optional[int] = Field(description="Id юзера")
    email: Optional[EmailStr] = Field(description="Email юзера")
    role: Optional[str] = Field(default="user", description="Role юзера")
    is_active: Optional[bool] = Field(default=True, description="Статус пользователя")
    date_joined: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: Optional[EmailStr] = Field(description="Email")
    password: Optional[str] = Field(min_length=8, description="Password, минимальный размер пороля 8")