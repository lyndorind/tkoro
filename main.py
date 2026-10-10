from fastapi import FastAPI

app = FastAPI(
    title="Git Lab 2 REST Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Service is running"}


@app.get("/info")
def info():
    return {
        "name": "Git Lab 2 REST Service",
        "version": "1.0.0"
    }