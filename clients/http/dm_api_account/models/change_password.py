from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    token: str = Field(..., description="Token")
    old_password: str = Field(None, alias='oldPassword')
    new_password: str = Field(None, alias='newPassword')

