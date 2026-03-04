from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exceptions.business_rule_exception import BusinessRuleException
from app.domain.exceptions.unauthorized_exception import UnauthorizedException
from starlette.exceptions import HTTPException as StarletteHTTPException

def initErrorHandler(app: FastAPI):
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