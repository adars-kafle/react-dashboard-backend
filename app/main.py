from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from app.api.routes import authentication, suppliers, users
from app.db import db_models
from app.db.database import engine

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # List of origins that are allowed to make requests to this API. Use "*" to allow all origins.
    allow_credentials=True,
    allow_methods=[
        "*"
    ],  # List of HTTP methods allowed (e.g., GET, POST, etc.). Use "*" to allow all methods.
    allow_headers=["*"],  # List of HTTP headers allowed. Use "*" to allow all headers.
)

# Create a main API router
main_router = APIRouter()


@app.get("/")
def root():
    return {"message": "Welcome to the API"}


# Include the suppliers routes
main_router.include_router(suppliers.routes, prefix="/suppliers", tags=["suppliers"])
main_router.include_router(users.routes, prefix="/user", tags=["user"])
main_router.include_router(authentication.routes, prefix="/auth", tags=["auth"])

# Include the main router under the /api path
app.include_router(main_router, prefix="/api")
