from uuid import UUID

from sqlmodel import SQLModel, Field


class BookUserRelationship(SQLModel, table=True):
    book_olid: str = Field(default=None, primary_key=True, foreign_key="bookedition.olid")
    user_uuid: UUID = Field(default=None, primary_key=True, foreign_key="user.uuid")
