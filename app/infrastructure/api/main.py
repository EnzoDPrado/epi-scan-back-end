from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.infrastructure.controllers import user_controller, epi_controller
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.domain.exceptions.business_rule_exception import BusinessRuleException
from app.domain.exceptions.unauthorized_exception import UnauthorizedException
from app.application.utils.ai_utils import organize_ai_train_folders, ai_train
from app.application.services.yolo_service import YoloService


# SERVER CONFIG
app = FastAPI()

# ROUTES
app.include_router(user_controller.router)
app.include_router(epi_controller.router)


# ORGANIZE AI FOLDERS
# organize_ai_train_folders()


# AI TRAIN
# ai_train()


# ERROR HANDLERS
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    message = first_error["msg"]
    
    return JSONResponse(
        status_code=400,  
        content={
            "message": f"Erro no campo '{field}': {message}"
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"Erro interno do servidor"
        }
    )


@app.exception_handler(BusinessRuleException)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc)
        }
    )


@app.exception_handler(UnauthorizedException)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={
            "message": str(exc)
        }
    )

app.include_router(user_controller.router)