import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse

from models.user import User
from utils.jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from routers.conversions import conversions_router
from config.database import engine, Base

# Load environment variables
load_dotenv()

# Create the FastAPI instance
app = FastAPI()
app.title = "Currency conversion"
app.version = "0.0.1"

# Add the error handler middleware
app.add_middleware(ErrorHandler)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Add the conversions router
app.include_router(conversions_router)

# Define the home endpoint
@app.get("/", tags=["home"])
def home():
    """
    Home endpoint.
    """
    return HTMLResponse('<h3>To use the app go to:</h3> <a href="/docs">Docs</a>')


# Define the login endpoint
@app.post("/login", tags=["auth"])
def login(user: User):
    """
    Login endpoint.
    """
    if user.id == os.environ.get("ID") and user.password == os.environ.get("PASSWORD"):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
