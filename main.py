from fastapi import FastAPI
import models
from database import engine
from routers import admin, auth, todos, users

app = FastAPI()


# will only run if the db file does not exist
models.Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def healthy():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
