from uuid import UUID

from sqlmodel import SQLModel, Field


class BookCollectionRelationship(SQLModel):
    book_uuid: UUID = Field(default=None, primary_key=True, foreign_key="book.uuid")
    collection_uuid: UUID = Field(
        default=None, primary_key=True, foreign_key="collection.uuid"
    )
