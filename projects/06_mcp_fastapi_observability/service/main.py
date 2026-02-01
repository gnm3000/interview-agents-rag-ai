import logging

from fastapi import FastAPI

from .routes import router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="MCP Hub", version="0.1.0")
app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
