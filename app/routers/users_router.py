from fastapi import APIRouter, HTTPException, Path, Depends, Body
from pony.orm import db_session
from typing_extensions import Annotated

from app.auth import get_current_user
from app.models import User
from app.schemas import UserOut, UserInUpdate
from app.utils import admin_required

router = APIRouter()


@router.get('/', response_model=list[UserOut])
async def get_users():
	with db_session:
		return list(User.select())


@router.get('/{user_name}', response_model=list[UserOut])
async def get_user(user_name: Annotated[str, Path(description="Имя пользователя", min_length=1, max_length=32)]):
	with db_session:
		users = list(User.select(name=user_name))

		return users


@router.patch("/{user_id}/role", response_model=UserOut)
async def change_user_role(
		user_id: Annotated[int, Path(gt=0)],
		new_role: Annotated[str, Body()],
		current_user: User = Depends(admin_required)):
	with db_session:
		user = User.get(id=user_id)
		if not user:
			raise HTTPException(status_code=404, detail="User not found")
		user.role = new_role
		return user


@router.patch("/me", response_model=UserOut)
async def update_me(
		user_update: Annotated[UserInUpdate, Body()],
		current_user: User = Depends(get_current_user)):
	with db_session:
		user = User.get(id=current_user.id)

		if not user:
			raise HTTPException(status_code=404, detail="User not found")

		user.name = user_update.name
		user.surname = user_update.surname

		return user
