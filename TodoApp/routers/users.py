from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from TodoApp.database import db_dependency
from TodoApp.models import Users

from .auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerification,
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(
        user_verification.password,
        user_model.hashed_password,  # type: ignore
    ):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(  # type: ignore
        user_verification.new_password
    )

    db.add(user_model)
    db.commit()
