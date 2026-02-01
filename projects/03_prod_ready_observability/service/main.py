from fastapi import FastAPI

from service.routes import router

app = FastAPI(title="Interview Service")
app.include_router(router)
