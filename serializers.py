from pydantic import BaseModel, Field, model_validator
from typing import Self


class ChangePasswordSerializer(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)
    new_password2: str = Field(min_length=8)

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.new_password != self.new_password2:
            raise ValueError("new_password and new_password2 do not match")
        return self

class UserSerializer(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=8)
    role: str = Field("user")


class TodoSerializer(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=200)
    priority: int = Field(ge=1, le=5)
    complete: bool = Field(False)


class TokenSerializer(BaseModel):
    access_token: str
    token_type: str
