from pydantic import BaseModel, Field

class Worker(BaseModel):
    id: int = Field(description="Worker ID")
    name: str = Field(description="Worker Name")
    is_active: bool = Field(description="Worker Status", default=True)

class WorkerCreate(BaseModel):
    name: str = Field(description="Worker Name")
    user_id: int = Field(description="Worker ID")