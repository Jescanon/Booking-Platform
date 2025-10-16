from pydantic import BaseModel, Field, ConfigDict



class Business(BaseModel):
    id: int = Field(description="Business ID")
    owner_id: int = Field(description="Business owner ID (ID юзера, кто владеет)")
    name: str = Field(description="Business Name")
    description: str | None = Field(max_length=255, description="Business Description")
    contacts: str | None = Field(max_length=255, description="Business Contacts")
    is_active: bool = Field(default=True, description="Business Active")

    model_config = ConfigDict(from_attributes=True)

class CreateBusiness(BaseModel):
    name: str = Field(description="Business Name")
    description: str | None = Field(max_length=255, description="Business Description")
    contacts: str | None = Field(max_length=255, description="Business Contacts")