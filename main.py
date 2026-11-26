from contextlib import asynccontextmanager

from db_api import init_db
from db_api import router as db_router
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Git Lab 2 REST Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(db_router)


@app.get("/")
def root():
    return {"message": "Service is running"}

@app.get("/info")
def info():
    return {
        "name": "Git Lab 2 REST Service",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Git Lab 2 REST Service"
    }

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}
