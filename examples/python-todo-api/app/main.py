from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="todo-api")
app.include_router(router)
