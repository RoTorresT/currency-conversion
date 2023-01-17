import os
from jwt import encode, decode


def create_token(data: dict) -> str:
    """
    Create a JWT token with the given data.

    Parameters:
        - data (dict): The data to include in the token
    Returns:
        - str: The JWT token
    """

    token: str = encode(
        payload=data, key=os.environ.get("SECRET_KEY"), algorithm="HS256"
    )
    return token


def validate_token(token: str) -> dict:
    """
    Validate a JWT token and return the data.

    Parameters:
        - token (str): The JWT token to validate
    Returns:
        - dict: The data included in the token
    """
    data: dict = decode(token, key=os.environ.get("SECRET_KEY"), algorithms=["HS256"])
    return data
