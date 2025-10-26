from uuid import UUID

from sqlmodel import SQLModel, Field


class BookAuthorRelationship(SQLModel):
    book_uuid: UUID = Field(default=None, primary_key=True, foreign_key="book.uuid")
    author_uuid: UUID = Field(default=None, primary_key=True, foreign_key="author.uuid")
