from fastapi import FastAPI, status
from app.infrastructure.api.router import initRouter
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.api.error_handler import initErrorHandler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initErrorHandler(app)
initRouter(app)

# ORGANIZE AI FOLDERS
# organize_ai_train_folders()


# AI TRAIN
# ai_train()
