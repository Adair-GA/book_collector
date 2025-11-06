from server.controller.book_controller import BookController
from server.controller.user_controller import UserController

user_controller = UserController()
book_controller = BookController()

def get_user_controller() -> UserController:
    return user_controller

def get_book_controller() -> BookController:
    return book_controller
