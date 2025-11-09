from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from server.api.dependencies import get_user_controller
from server.api.security import Token
from server.api.utils.generic_success_response import GenericSuccessResponse
from server.controller.exceptions.users.email_already_registered_exception import (
    EmailAlreadyRegisteredException,
)
from server.controller.exceptions.users.incorrect_password_exception import (
    IncorrectPasswordException,
)
from server.controller.exceptions.users.invalid_email_exception import (
    InvalidEmailException,
)
from server.controller.exceptions.users.user_not_found_exception import (
    UserNotFoundException,
)
from server.controller.user_controller import UserController

user_router = APIRouter()
user_controller_dependency = Annotated[UserController, Depends(get_user_controller)]


class RegisterRequest(BaseModel):
    email: str
    password: str


@user_router.post(
    "/register",
    responses={
        200: {"model": GenericSuccessResponse},
        400: {"model": GenericSuccessResponse},
    },
    response_model_exclude_none=True,
)
async def register(
    request: RegisterRequest,
    response: Response,
    user_controller: user_controller_dependency,
) -> GenericSuccessResponse:
    try:
        await user_controller.create_user(request.email, request.password)
    except (InvalidEmailException, EmailAlreadyRegisteredException) as e:
        response.status_code = 400
        return GenericSuccessResponse(success=False, info=e.__class__.__name__)

    return GenericSuccessResponse(success=True)


@user_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_controller: user_controller_dependency,
) -> Token:
    try:
        jwt_token = await user_controller.login(form_data.username, form_data.password)
    except (UserNotFoundException, IncorrectPasswordException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=jwt_token, token_type="bearer")
