from config.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, VARCHAR


class TransactionsModel(Base):
    """
    SQLAlchemy model for the transactions table
    """

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    converted_amount = Column(Float)
    rate = Column(Float)
    time_of_conversion = Column(Integer)
    from_currency = Column(VARCHAR(3))
    to_currency = Column(VARCHAR(3))

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "converted_amount": 24.12313,
                "rate": 1.1034,
                "time_of_conversion": "2022-12-31T23:59:59",
                "from_currency": "USD",
                "to_currency": "EUR",
            }
        }
