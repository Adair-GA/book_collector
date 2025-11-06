from datetime import timedelta, datetime, timezone
from uuid import UUID

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from email_validator import validate_email, EmailNotValidError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .db.db_provider import sql_async_engine
from .exceptions.users.email_already_registered_exception import (
    EmailAlreadyRegisteredException,
)
from .exceptions.users.incorrect_password_exception import IncorrectPasswordException
from .exceptions.users.invalid_email_exception import InvalidEmailException
from .exceptions.users.user_not_found_exception import UserNotFoundException
from .shared_config import SharedConfig
from .. import User


class UserController:
    def __init__(self):
        self.async_engine = sql_async_engine
        self.password_hasher = PasswordHash([Argon2Hasher()])

    async def create_user(self, email: str, password: str):
        try:
            validate_email(email)
        except EmailNotValidError:
            raise InvalidEmailException()
        async with AsyncSession(self.async_engine) as session:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            existing_user = result.one_or_none()
            if existing_user:
                raise EmailAlreadyRegisteredException()

            hashed_password = self.password_hasher.hash(password)
            new_user = User(email=email, password=hashed_password)
            session.add(new_user)
            await session.commit()

    async def find_user_by_id(self, user_uuid: UUID) -> User | None:
        async with AsyncSession(self.async_engine) as session:
            statement = select(User).where(User.uuid == user_uuid)
            result = await session.exec(statement)
            user = result.one_or_none()

        return user

    async def login(self, email: str, password: str) -> str:
        """
        Logs in a auth and returns a JWT token valid for 14 days.
        :param email:
        :param password:
        :return: JWT token valid for 14 days
        :raises IncorrectPasswordException: If provided password is incorrect
        """
        async with AsyncSession(self.async_engine) as session:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            existing_user = result.one_or_none()

        if existing_user is None:
            raise UserNotFoundException()

        if not self.password_hasher.verify(password, existing_user.password):
            raise IncorrectPasswordException()

        access_token_expires = timedelta(days=14)
        encoded_jwt = jwt.encode(
            {
                "sub": str(existing_user.uuid),
                "exp": datetime.now(tz=timezone.utc) + access_token_expires,
            },
            key=SharedConfig.jwt_secret,
            algorithm=SharedConfig.jwt_algorithm,
        )

        return encoded_jwt
