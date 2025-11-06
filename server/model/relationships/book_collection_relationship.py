from uuid import UUID

from sqlmodel import SQLModel, Field


class BookCollectionRelationship(SQLModel, table=True):
    book_olid: str = Field(default=None, primary_key=True, foreign_key="book.olid")
    collection_uuid: UUID = Field(
        default=None, primary_key=True, foreign_key="collection.uuid"
    )
