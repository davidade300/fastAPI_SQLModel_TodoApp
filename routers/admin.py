from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from database import db_dependency
from models import Todos

from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not Found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()