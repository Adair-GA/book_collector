
from sqlmodel import SQLModel, Field


class BookEdition(SQLModel, table=True):
    olid: str = Field(default=None, primary_key=True)
    work_olid: str = Field(foreign_key="book.olid")
    title: str | None
    cover: str | None
    ISBN10: str | None = Field(index=True)
    ISBN13: str | None = Field(index=True)
    language: str | None
