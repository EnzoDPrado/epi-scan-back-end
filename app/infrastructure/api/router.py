from fastapi import FastAPI
from app.infrastructure.controllers import user_controller, epi_controller

def initRouter(app: FastAPI) :
    app.include_router(user_controller.router)
    app.include_router(epi_controller.router)
