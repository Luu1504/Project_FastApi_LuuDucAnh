from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import (
    health_router,
    auth_router,
    users_router,
    club_router,
    activity_router,
)
from app.models import User, Club, ClubMember, ClubActivity

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Club Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def format_response(status_code: int, message: str, data=None, error=None):
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
        "error": error,
    }


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


app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(club_router, prefix="/api/v1")
app.include_router(activity_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Student Club Management API", "docs": "/docs"}
