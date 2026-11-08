from pydantic import BaseModel, Field


class UserSerializer(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str = Field("user")


class TodoSerializer(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=200)
    priority: int = Field(ge=1, le=5)
    complete: bool = Field(False)


class TokenSerializer(BaseModel):
    access_token: str
    token_type: str
