from typing import Union

from fastapi import Depends
from fastapi_users import (IntegerIDMixin,
                           BaseUserManager,
                           FastAPIUsers,
                           InvalidPasswordException)
from fastapi_users.authentication import (BearerTransport,
                                          JWTStrategy,
                                          AuthenticationBackend)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate
from app.core.db import get_async_session
from app.core.config import settings


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                # текстова из тестов
                reason="Password should be at least 3 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='/auth/jwt/login')


def get_jwt_stategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt_auth_backend',
    transport=bearer_transport,
    get_strategy=get_jwt_stategy
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
