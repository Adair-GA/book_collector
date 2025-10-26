from server.controller.user_controller import UserController

user_controller = UserController()


def get_user_controller() -> UserController:
    return user_controller
