from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class Collection(SQLModel, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    owner_uuid: UUID = Field(default=None, foreign_key="user.uuid")
    description: str = ""
