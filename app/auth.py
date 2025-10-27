import os
from datetime import timedelta, timezone, datetime
from typing import Annotated

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pony.orm import db_session
from starlette import status
from pwdlib import PasswordHash
import jwt

from app.schemas import UserInDbFull
from app.models import User

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


o2auth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

pass_hash = PasswordHash.recommended()

credentials_exception = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Incorrect username or password",
	headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:
	return pass_hash.verify(plain_pass, hashed_pass)


def get_pass_hash(plain_pass: str) -> str:
	return pass_hash.hash(plain_pass)


def create_token(data: dict, exp_time: timedelta) -> str:
	encoded_jwt = data.copy()
	encoded_jwt['exp'] = datetime.now(timezone.utc) + exp_time

	return jwt.encode(encoded_jwt, SECRET_KEY, ALGORITHM)


def get_user_from_db(email: str) -> User | None:
	with db_session():
		user = User.get(email=email)

		if not user:
			raise credentials_exception

		return user


async def get_current_user(token: Annotated[str, Depends(o2auth_scheme)]) -> UserInDbFull:
	try:
		data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		email = data.get("sub")

		if email is None:
			raise credentials_exception

		user = get_user_from_db(email)

		if not user.is_active:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

		return user
	except jwt.InvalidTokenError:
		raise credentials_exception



async def auth_user(email: str, password: str) -> UserInDbFull:
	user = get_user_from_db(email)

	if not verify_password(password, user.password):
		raise credentials_exception

	return user