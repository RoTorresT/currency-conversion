import os
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    """
    Custom JWTBearer class that validates the token with the validate_token function
    and compares the data with the environment variables
    """

    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["id"] != os.environ.get("ID") or data["password"] != os.environ.get(
            "PASSWORD"
        ):
            raise JSONResponse(
                status_code=403, content={"error": "Invalid credentials"}
            )
