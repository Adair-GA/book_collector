from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.operators import ilike_op
from sqlmodel import select, or_
from sqlmodel.ext.asyncio.session import AsyncSession

from server import BookEdition, Collection
from server.controller.db.db_provider import sql_async_engine
from server.controller.exceptions.books.book_not_found_exception import BookNotFound
from server.controller.exceptions.collections.collection_not_found_exception import (
    CollectionNotFoundException,
)
from server.controller.exceptions.collections.collection_not_owned_exception import (
    CollectionNotOwnedException,
)
from server.model.relationships.book_collection_relationship import (
    BookCollectionRelationship,
)
from server.model.relationships.book_user_relationship import BookUserRelationship


class BookController:
    def __init__(self):
        self._async_engine = sql_async_engine
        # self._fetcher = OpenLibraryFetcher()

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
    #             # noinspection PyTypeChecker
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
    #
    #             session.add(book)
    #             session.add_all(authors)
    #             session.add_all(editions)
    #
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

    async def search_book_by_title(self, title: str) -> list[BookEdition]:
        async with AsyncSession(self._async_engine) as session:
            statement = select(BookEdition).where(
                ilike_op(BookEdition.title, f"%{title}%"),
            )

            result = await session.exec(statement)
            books = result.all()

        return list(books)

    async def find_book_by_olid(self, olid: str) -> BookEdition | None:
        async with AsyncSession(self._async_engine) as session:
            statement = select(BookEdition).where(BookEdition.olid == olid)

            result = await session.exec(statement)
            book = result.one_or_none()

        return book

    async def add_book_to_user_by_olid(self, user_uuid: UUID, book_olid: str):
        if not await self.find_book_by_olid(book_olid):
            raise BookNotFound()
        try:
            async with AsyncSession(self._async_engine) as session:
                book_user = BookUserRelationship(user_uuid=user_uuid, book_olid=book_olid)
                session.add(book_user)

                await session.commit()

        except IntegrityError:
            pass

    async def get_user_books(self, user_uuid: UUID) -> list[BookEdition]:
        async with AsyncSession(self._async_engine) as session:
            query = select(BookEdition, BookUserRelationship).where(
                BookUserRelationship.user_uuid == user_uuid,
                BookUserRelationship.book_olid == BookEdition.olid,
            )
            result = await session.exec(query)

            user_books = result.all()

        books = [book for book, _ in user_books]
        print(books)
        return books

    async def create_collection(
        self, user_uuid: UUID, name: str, description: str | None
    ):
        collection = Collection(
            title=name, description=description, owner_uuid=user_uuid
        )

        with AsyncSession(self._async_engine) as session:
            session.add(collection)
            await session.commit()

    async def get_collection_by_id(self, uuid: UUID) -> Collection | None:
        with AsyncSession(self._async_engine) as session:
            statement = select(Collection).where(Collection.uuid == uuid)
            result = await session.exec(statement)
            collection = result.one_or_none()

            return collection

    async def add_book_to_collection(
        self, user_uuid: UUID, book_olid: str, collection_id: UUID
    ):
        collection = await self.get_collection_by_id(collection_id)
        book = await self.find_book_by_olid(book_olid)

        if not book:
            raise BookNotFound()

        if not collection:
            raise CollectionNotFoundException()

        if collection.owner_uuid != user_uuid:
            raise CollectionNotOwnedException()

        relationship = BookCollectionRelationship(
            book_olid=book_olid, collection_uuid=collection.uuid
        )

        try:
            with AsyncSession(self._async_engine) as session:
                session.add(relationship)

                await session.commit()
        except IntegrityError:
            pass
