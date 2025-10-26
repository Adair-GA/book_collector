from pydantic import BaseModel


class GenericSuccessResponse(BaseModel):
    success: bool
    info: str | None = None
