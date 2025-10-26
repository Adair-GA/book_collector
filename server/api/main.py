from typing import Annotated

from fastapi import FastAPI, Depends

from .routes.user.user_router import user_router
from .security import get_current_user
from .. import User
from ..controller.db.db_provider import init_db

init_db()
app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["login"])


@app.get("/", tags=["root"])
async def root(current_user: Annotated[User, Depends(get_current_user)]):
    return {"message": f"Welcome to your book collector {current_user.email}!"}
