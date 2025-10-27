from pony.orm import Required, PrimaryKey

from app.db import db


class User(db.Entity):
	id = PrimaryKey(int, auto=True)
	name = Required(str)
	surname = Required(str)
	email = Required(str, unique=True)
	password = Required(str)
	role = Required(str, default="user")
	is_active = Required(bool, default=True)
