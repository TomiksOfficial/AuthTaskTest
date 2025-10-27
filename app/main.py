from contextlib import asynccontextmanager

from fastapi import FastAPI
from pony.orm import set_sql_debug

from app.db import db
from app.routers import users_router, auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
	db.generate_mapping(create_tables=True)
	set_sql_debug(True)

	yield

	db.disconnect()


fapi = FastAPI(lifespan=lifespan)

fapi.include_router(users_router.router, prefix='/users', tags=['users'])
fapi.include_router(auth_router.router, prefix='/auth', tags=['auth'])
