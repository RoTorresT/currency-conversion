import re

from pydantic import BaseModel, validator
from iso4217 import Currency as IsoCurrency  # Currency.usd.code


class Currency(str):
    """
    A custom Pydantic field for currency codes, using the iso4217 library to validate codes.
    """

    pattern = re.compile(r"^[a-zA-Z]{3}$")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not cls.pattern.match(value):
            raise ValueError(f"Invalid currency code: {value}")

        try:
            return getattr(IsoCurrency, value.lower()).code

        except AttributeError as e:
            raise ValueError(f"Invalid currency code: {value}")


class ConvertModel(BaseModel):
    """
    Pydantic Model for conversion data
    """

    amount: float
    from_currency: Currency
    to_currency: Currency

    @validator("amount")
    def amount_is_positive(cls, value):
        """
        Validate that the amount is a positive number
        """
        if value < 0:
            raise ValueError("Amount must be a positive number")
        return value
