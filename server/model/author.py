from uuid import UUID
from sqlmodel import SQLModel, Field


class Author(SQLModel, table=True):
    uuid: UUID = Field(default=None, primary_key=True)
    name: str
