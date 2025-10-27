from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field, EmailStr

if TYPE_CHECKING:
	from app.models import Task

AUserName = Annotated[str, Field(description="Имя/Фамилия пользователя", min_length=1, max_length=32)]
AUserId = Annotated[int, Field(description="ID пользователя", gt=0)]
ARole = Annotated[str, Field(description="Роль пользователя", min_length=1, max_length=32)]
AIsActive = Annotated[bool, Field(description="Активен ли аккаунт")]


class UserBase(BaseModel):
	id: AUserId
	name: AUserName
	surname: AUserName
	role: ARole
	is_active: AIsActive


class UserIn(BaseModel):
	name: AUserName
	surname: AUserName
	email: EmailStr
	password: Annotated[str, Field(description="Пароль для регистрации", min_length=1, max_length=32)]


class UserInUpdate(BaseModel):
	name: AUserName
	surname: AUserName


class UserOut(UserBase):
	pass


class UserInDB(UserBase):
	role: ARole
	password: Annotated[str, Field(description="Хешированный пароль")]


class UserInDbFull(UserOut, UserInDB):
	pass


class TokenOut(BaseModel):
	access_token: str
	token_type: str
