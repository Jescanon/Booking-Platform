from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class Booking(BaseModel):
    id: int = Field(description="Id of the booking")
    user_id: int = Field(description="Id of the user")
    service_id: int = Field(description="Id of the service")
    worker_id: int = Field(description="Id of the worker")

    start_time: datetime = Field(description="Start time of the booking")
    status: str = Field(description="Status of the booking", default="waiting")

    model_config = ConfigDict(from_attributes=True)

class CreateBooking(BaseModel):
    service_id: int = Field(description="Id of the service")
    worker_id: int = Field(description="Id of the worker")

    start_time: datetime = Field(description="Start time of the booking")