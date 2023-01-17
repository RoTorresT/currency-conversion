from pydantic import BaseModel


class User(BaseModel):
    """
    Pydantic model for a User
    """

    id: str
    password: str
