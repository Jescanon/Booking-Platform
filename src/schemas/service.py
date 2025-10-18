from pydantic import BaseModel, Field, ConfigDict


class Service(BaseModel):
    id: int = Field(description="ID of service")
    business_id: int = Field(description="ID владельца бизнеса")
    name: str = Field(description="Имя заказа")
    duration: int = Field(description="Продолжительность")
    price: int = Field(description="Цена товара")
    is_active: bool

    config = ConfigDict(from_attributes=True)

class ServiceCreat(BaseModel):
    name: str = Field(description="Имя заказа")
    duration: int = Field(description="Продолжительность")
    price: int = Field(description="Цена товара")