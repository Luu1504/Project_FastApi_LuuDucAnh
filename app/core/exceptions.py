from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


def format_response(status_code: int, message: str, data=None, error=None):
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
        "error": error,
    }


def setup_exceptions(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=format_response(
                status_code=exc.status_code,
                message=str(exc.detail),
                error="HTTP Error",
            ),
        )
