from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str | None = None
    user_id: str | None = None