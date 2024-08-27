from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path, status
import TodoApp.models as models
from TodoApp.database import SessionLocal, engine
from sqlalchemy.orm import Session
from TodoApp.models import Todos

app = FastAPI()

# will only run if the db file does not exist
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
# Depends -> dependency injection
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found!")

    return todo_model
