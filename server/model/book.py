
from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    olid: str = Field(default=None, primary_key=True)
    title: str
