from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.core.exceptions import setup_exceptions
from app.routers.health import router as health_router
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

setup_exceptions(app)

app.include_router(health_router)
app.include_router(health_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Student Club Management API", "docs": "/docs"}
