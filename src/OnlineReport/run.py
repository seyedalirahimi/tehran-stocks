from concurrent.futures.thread import ThreadPoolExecutor

import requests

import tehran_stocks.config as db
from tehran_stocks import Stocks
from utils import utils

if __name__ == "__main__":
    stocks = db.session.query(Stocks.code).all()

    with ThreadPoolExecutor(max_workers=1   ) as executor:
        for i, code in enumerate(stocks):
            id = code[0]

            response = requests.get(
                f"http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={id}&c=44%20", timeout=5
            )

            print(f'{i},{id},{response.text}')
