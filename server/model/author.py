from sqlmodel import SQLModel, Field


class Author(SQLModel, table=True):
    olid: str = Field(default=None, primary_key=True)
    name: str
