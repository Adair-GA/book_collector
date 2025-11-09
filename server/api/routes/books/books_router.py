from server.model.book_edition import BookEdition


from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import Response

from server.api.dependencies import get_book_controller
from server.api.security import current_user_dependency
from server.api.utils.generic_success_response import GenericSuccessResponse
from server.controller.book_controller import BookController
from server.controller.exceptions.books.book_not_found_exception import BookNotFound

book_router = APIRouter()
book_controller_dependency = Annotated[BookController, Depends(get_book_controller)]


# noinspection PyTypeHints
@book_router.get(
    "/search",
    responses={
        200: {"model": list[BookEdition]},
        400: {"model": GenericSuccessResponse},
    },
)
async def search_book(
    book_controller: book_controller_dependency,
    _current_user: current_user_dependency,
    response: Response,
    isbn: str | None = None,
    title: str | None = None,
):
    if isbn and len(isbn) != 10 and len(isbn) != 13:
        response.status_code = 400
        return GenericSuccessResponse(success=False, info="ISBN not valid")

    if isbn:
        book = await book_controller.search_book_by_isbn(
            isbn_10=isbn if len(isbn) == 10 else None,
            isbn_13=isbn if len(isbn) == 13 else None,
        )
        if book:
            books = [book]
        else:
            books = []

    elif title:
        books = await book_controller.search_book_by_title(title)
    else:
        response.status_code = 400
        return GenericSuccessResponse(success=False, info="Provide isbn or title")

    return books


@book_router.post(
    "/add",
    responses={
        200: {"model": GenericSuccessResponse},
        404: {"model": GenericSuccessResponse},
    },
)
async def add_book(
    book_controller: book_controller_dependency,
    book_olid: str,
    current_user: current_user_dependency,
    response: Response,
) -> GenericSuccessResponse:
    try:
        await book_controller.add_book_to_user_by_olid(
            book_olid=book_olid, user_uuid=current_user.uuid
        )

        return GenericSuccessResponse(success=True)
    except BookNotFound:
        response.status_code = 404
        return GenericSuccessResponse(success=False, info="Book not found")


@book_router.get("/my_books")
async def get_my_books(
    book_controller: book_controller_dependency,
    current_user: current_user_dependency,
) -> list[BookEdition]:
    return await book_controller.get_user_books(user_uuid=current_user.uuid)
