from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pony.orm import db_session
from starlette import status

from app.auth import auth_user, create_token, get_current_user, get_pass_hash
from app.models import User
from app.schemas import TokenOut, UserOut, UserIn

router = APIRouter()
TOKEN_EXPIRE_MINUTES = 15


@router.post('/token', response_model=TokenOut)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	await auth_user(form_data.username, form_data.password)

	token_exp = timedelta(minutes=TOKEN_EXPIRE_MINUTES)

	token = create_token(
		data={'sub': form_data.username},
		exp_time=token_exp
	)

	return TokenOut(access_token=token, token_type='bearer')


@router.post('/register', response_model=UserOut)
async def register(user_data: Annotated[UserIn, Body(description="Данные для регистрации")]):
	with db_session:
		if User.select(email=user_data.email).count() > 0:
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail="The email is already in use"
			)

		user = User(name=user_data.name, surname=user_data.surname, email=user_data.email,
					password=get_pass_hash(user_data.password), role="user")

		return user


@router.delete('/remove', response_model=UserOut)
async def remove_me(current_user: Annotated[User, Depends(get_current_user)]):
	with db_session:
		user = User.get(email=current_user.email)

		user.is_active = False

		return user


@router.get('/me', response_model=UserOut)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
	return current_user
