from uuid import UUID

from sqlmodel import SQLModel, Field


class BookEdition(SQLModel, table=True):
    uuid: UUID = Field(default=None, primary_key=True)
    book_uuid: UUID = Field(default=None, foreign_key="book.uuid")
    title: str
    cover: str
    ISBN10: str
    ISBN13: str | None
    language: str
