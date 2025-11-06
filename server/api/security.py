from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status

from server import User
from server.api.dependencies import get_user_controller
from server.controller.shared_config import SharedConfig
from server.controller.user_controller import UserController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_uuid: str | None = None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_controller: Annotated[UserController, Depends(get_user_controller)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SharedConfig.jwt_secret, algorithms=[SharedConfig.jwt_algorithm])
        user_uuid = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
        token_data = TokenData(user_uuid=user_uuid)
    except InvalidTokenError:
        raise credentials_exception
    user = await user_controller.find_user_by_id(user_uuid=UUID(token_data.user_uuid))
    if user is None:
        raise credentials_exception
    return user


current_user_dependency = Annotated[User, Depends(get_current_user)]
