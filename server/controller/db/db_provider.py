from sqlmodel import create_engine, SQLModel

sql_engine = create_engine("sqlite:///books.db", echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(sql_engine)
