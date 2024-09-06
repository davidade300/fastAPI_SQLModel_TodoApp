from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from TodoApp.database import db_dependency
from TodoApp.models import Users

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "dfbc7d1080a2ac039ffc104e2372b6251cd9228dcefe8c13649eace2dd5a0b24"
ALGORITHM = "HS256"

# default information needed to passlib to work properly
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):  # type: ignore
        return False

    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        user_id: int = payload.get("id")  # type: ignore
        user_role: str = payload.get("role")  # type: ignore
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user!",
            )

        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user!",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
# it's not possible to pass the  CreateUserRequest through model_dump
# so it's better to just pass it manually
async def create_users(
    create_user_request: CreateUserRequest, db: db_dependency
):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post(
    "/token", response_model=Token, status_code=status.HTTP_202_ACCEPTED
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user!",
        )

    token = create_access_token(
        user.username,  # type: ignore
        user.id,  # type: ignore
        user.role,  # type: ignore
        timedelta(minutes=20),  # type: ignore
    )

    return {"access_token": token, "token_type": "bearer"}
