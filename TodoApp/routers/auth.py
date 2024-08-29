from fastapi import APIRouter
from pydantic import BaseModel

from TodoApp.models import Users

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth")
# it's not possible to pass the  CreateUserRequest through model_dump
# so it's better to just pass it manually
async def create_users(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=create_user_request.password,
        is_active=True,
    )
    return create_user_model
