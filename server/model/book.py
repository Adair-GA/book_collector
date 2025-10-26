from uuid import UUID

from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    uuid: UUID = Field(default=None, primary_key=True)
    title: str
    cover: str
    ISBN10: str
    ISBN13: str | None
    language: str
