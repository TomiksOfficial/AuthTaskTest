from typing import Annotated

from fastapi import Depends, HTTPException

from app.auth import get_current_user
from app.models import User

CurrentUserId = Annotated[int, Depends(get_current_user)]

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user