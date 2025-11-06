from collections.abc import Collection

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from server import Author, Book, BookEdition
from server.controller.db.db_provider import sql_async_engine
# from server.controller.open_library_fetch.open_library_fetcher import OpenLibraryFetcher
# from server.controller.open_library_fetch.openlibrary_book import OpenlibraryBook


class BookController:
    def __init__(self):
        self._async_engine: AsyncEngine = sql_async_engine
        # self._fetcher: OpenLibraryFetcher = OpenLibraryFetcher()

    # async def _save_from_ol(self, books: Collection[OpenlibraryBook]):
    #     async with AsyncSession(self._async_engine) as session:
    #         for ol_book in books:
    #             book = Book(olid=ol_book.key, title=ol_book.title)
    #             authors = [
    #                 Author(olid=author_key, name=author_name)
    #                 for author_key, author_name in zip(
    #                     ol_book.author_names, ol_book.author_keys
    #                 )
    #             ]
    #             editions = [
    #                 BookEdition(
    #                     olid=edition,
    #                     work_olid=book.olid,
    #                     title=book.title,
    #                     cover=ol_book.cover_url(),
    #                     ISBN10=None,
    #                     ISBN13=None,
    #                     language=ol_book.languages[0],
    #                 )
    #                 for edition in ol_book.editions
    #             ]

    #             session.add(book)
    #             session.add_all(authors)
    #             session.add_all(editions)

    #         await session.commit()

    async def search_book_by_isbn(
        self, isbn_10: str | None = None, isbn_13: str | None = None
    ) -> BookEdition | None:
        if not (isbn_10 or isbn_13):
            raise ValueError("ISBN10 or ISBN13 must be provided")

        async with AsyncSession(self._async_engine) as session:
            statement = select(BookEdition).where(
                or_(BookEdition.ISBN10 == isbn_10, BookEdition.ISBN13 == isbn_13)
            )
            result = await session.exec(statement)
            book = result.one_or_none()

        return book
