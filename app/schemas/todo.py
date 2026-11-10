from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=200)
    priority: int = Field(ge=1, le=5)
    complete: bool = Field(False)
