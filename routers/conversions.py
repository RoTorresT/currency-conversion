from datetime import datetime
from threading import Thread
from iso4217 import Currency as IsoCurrency  # Currency.usd.code

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.conversion import ConvertModel as ConversionData
from utils.scraping import Scraping
from config.database import Session
from services.conversions import add_transaction, get_transactions
from utils.utils import rebuild_metadata
from middlewares.jwt_bearer import JWTBearer


conversions_router = APIRouter()

# Global variable to avoid creating a new instance of the Scraping class
@conversions_router.on_event("startup")
async def init_scraping_class():
    """
    Initialize the Scraping class to avoid creating a new instance of the class
    """
    global scraping
    scraping = Scraping()


# Define conversion endpoint
@conversions_router.post(
    "/convert", tags=["conversion tool"], dependencies=[Depends(JWTBearer())]
)
def converted_amount_and_midmarket_rate(post_data: ConversionData) -> dict:
    """
    Convert an amount from one currency to another.

    Parameters:
        - post_data (ConversionData): amount(float), from_currency(str), to_currency(str)
    Returns:
        - dict: converted_amount(float), rate(float), metadata(dict: time_of_conversion(datetime), from_currency(str), to_currency(str)
    """

    mid_market_data = scraping.get_midmarket()

    try:
        rate_from_currency = mid_market_data.get("rates", None).get(
            post_data.from_currency, None
        )
        rate_to_currency = mid_market_data.get("rates", None).get(
            post_data.to_currency, None
        )

        if rate_from_currency is None:
            raise Exception(
                f"Currency id {post_data.from_currency} correct but not supported"
            )

        if rate_to_currency is None:
            raise Exception(
                f"Currency id {post_data.to_currency} correct but not supported"
            )

        rate = rate_to_currency / rate_from_currency
        converted_amount = post_data.amount * rate

        response = {
            "converted_amount": converted_amount,
            "rate": rate,
            "metadata": {
                "time_of_conversion": str(datetime.now()),
                "from_currency": post_data.from_currency,
                "to_currency": post_data.to_currency,
            },
        }
        Thread(target=add_transaction, args=(Session(), response)).start()

        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Define endpoint to get the supported currencies
@conversions_router.get(
    "/currencies", tags=["conversion tool"], dependencies=[Depends(JWTBearer())]
)
def get_all_supported_currencies():
    """
    Get all the supported currencies from the cache or from the API.

    Returns:
        - dict: supported_currencies(list)
    """
    mid_market_data = scraping.get_midmarket()
    supported_currencies_list = list(mid_market_data.get("rates", None).keys())
    
    response = {}
    
    supported_currencies_list = list(set(supported_currencies_list))
    for i in supported_currencies_list:

        try:
            response[getattr(IsoCurrency, i.lower()).currency_name] = getattr(IsoCurrency, i.lower()).code
        except:
            response[i.upper()] = None
            
        
    return JSONResponse(content=response, status_code=200)


# Define endpoint to get all previously made conversions
@conversions_router.get(
    "/history", tags=["conversion tool"], dependencies=[Depends(JWTBearer())]
)
def get_all_previously_made_conversions():
    """
    Get all the previously made conversions from the sqlite database.

    Returns:
        - dict: converted_amount(float), rate(float), metadata(dict: time_of_conversion(datetime), from_currency(str), to_currency(str)
    """
    result = get_transactions(Session())
    response = jsonable_encoder(result)
    for i in range(len(response)):
        response[i] = rebuild_metadata(response[i])

    return JSONResponse(status_code=200, content=response)
