from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import Response

from server.api.dependencies import get_book_controller
from server.api.security import current_user_dependency
from server.api.utils.generic_success_response import GenericSuccessResponse
from server.controller.book_controller import BookController

book_router = APIRouter()
book_controller_dependency = Annotated[BookController, Depends(get_book_controller)]


# noinspection PyTypeHints
@book_router.get("/search")
async def search_book(
    book_controller: book_controller_dependency,
    _current_user: current_user_dependency,
    isbn: str,
    response: Response,
):
    if len(isbn) != 10 and len(isbn) != 13:
        response.status_code = 400
        return GenericSuccessResponse(success=False)

    books = await book_controller.search_book_by_isbn(
        isbn_10=isbn if len(isbn) == 10 else None,
        isbn_13=isbn if len(isbn) == 13 else None,
    )

    return books
