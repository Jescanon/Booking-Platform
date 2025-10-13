from pydantic import BaseModel, Field, ConfigDict
from typing import Optional



class Business(BaseModel):
    id: Optional[int] = Field(description="Business ID")
    owner_id: Optional[int] = Field(description="Business owner ID (ID юзера, кто владеет)")
    name: Optional[str] = Field(description="Business Name")
    description: Optional[str | None] = Field(max_length=255, description="Business Description")
    contacts: Optional[str | None] = Field(max_length=255, description="Business Contacts")
    is_active: Optional[bool] = Field(default=True, description="Business Active")

    model_config = ConfigDict(from_attributes=True)

class CreateBusiness(BaseModel):
    name: Optional[str] = Field(description="Business Name")
    description: Optional[str | None] = Field(max_length=255, description="Business Description")
    contacts: Optional[str | None] = Field(max_length=255, description="Business Contacts")