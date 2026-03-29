# from pydantic import BaseModel

# class WebHookPayload(BaseModel):
#     event: str
#     data: int | None = None

from pydantic import BaseModel


class WebHookPayload(BaseModel):
    event: str
    data: int | None = None