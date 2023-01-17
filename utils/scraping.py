from fake_headers import Headers
import datetime
import time
import requests_cache
from typing import Dict, Tuple
from retry import retry


class Scraping:
    """
    Scraping class to get the midmarket value from the xe.com website
    """

    def __init__(self) -> None:
        """
        Initialize the class and create a session and fake headers generator.
        The decision to use a session with cache is because the behavior of the
        website, their endpoint updates every ~60s, so it is not necessary to
        make a request every time data is needed. The cache is stored in ram
        memory, so it is not necessary to use a database and its faster.
        
        """
        self.session = requests_cache.CachedSession(expire_after=10, backend="memory")
        self.fake_header_generator = Headers()

    @retry(delay=5, tries=2)
    def get_midmarket(self) -> Tuple[Dict, str]:
        """
        Get the midmarket value and returns it as a json object

        Returns:
            - Tuple (Dict, str): The midmarket value as json object and date of the last update
        """
        headers_1 = {
            "authority": "www.xe.com",
            "accept-language": "en-US,en;q=0.9,es;q=0.8",
            "authorization": "Basic bG9kZXN0YXI6akZiaFcyQWJvMU13VFQ0T2hDSDR1TUttT3pCUnY0ZmI=",
            "if-none-match": '"10dc-z6WX2wnzUoKeb3IUCcQq3rOadOU"',
            "referer": "https://www.xe.com/",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

        headers_2 = self.fake_header_generator.generate()

        d1 = headers_1.copy()
        d2 = headers_2.copy()
        headers_dict = {**d1, **d2}

        response = self.session.get(
            "https://www.xe.com/api/protected/midmarket-converter/",
            headers=headers_dict,
        )

        if response.status_code == 200:
            midmarket_json = response.json()

            return midmarket_json

        else:
            raise Exception(f"Error: {response.status_code}")
