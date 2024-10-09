from fastapi import FastAPI, Request, status
from starlette.status import HTTP_302_FOUND

from .Router import auth, todos, admin, users
from .database import engine
from .models import Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")


@app.get("/")
def test(request: Request,):
    return RedirectResponse("/todos/todo-page",status_code=HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
