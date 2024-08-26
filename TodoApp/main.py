from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from TodoApp.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the database at the startup of the fastapi App
    # if the models are not imported a empty database will be created
    import TodoApp.models  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
