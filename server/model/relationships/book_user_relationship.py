from uuid import UUID

from sqlmodel import SQLModel, Field


class BookUserRelationship(SQLModel):
    book_uuid: UUID = Field(default=None, primary_key=True, foreign_key="book.uuid")
    user_uuid: UUID = Field(default=None, primary_key=True, foreign_key="user.uuid")
