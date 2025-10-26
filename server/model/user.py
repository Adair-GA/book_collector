from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    uuid: UUID = Field(primary_key=True, default_factory=uuid4)
    email: str
    password: str | None
    google_oauth_token: str | None
