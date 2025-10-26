from uuid import UUID

from sqlmodel import SQLModel, Field


class Collection(SQLModel, table=True):
    uuid: UUID = Field(default=None, primary_key=True)
    title: str
    owner_uuid: UUID = Field(default=None, foreign_key="user.uuid")
    description: str = ""
