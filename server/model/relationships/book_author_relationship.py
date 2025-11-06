
from sqlmodel import SQLModel, Field


class BookAuthorRelationship(SQLModel, table=True):
    book_olid: str = Field(default=None, primary_key=True, foreign_key="book.olid")
    author_olid: str = Field(default=None, primary_key=True, foreign_key="author.olid")
