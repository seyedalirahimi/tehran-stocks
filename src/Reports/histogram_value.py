import tehran_stocks.config as db
import matplotlib.pyplot as plt
from tehran_stocks import Stocks
import pandas as pd
import matplotlib.ticker as mtick
from bidi.algorithm import get_display
import arabic_reshaper
import pathlib


def histogram_value(history_len):
    q = f"select date_shamsi,SUM(value) as value  from stock_price group by dtyyyymmdd order by date_shamsi desc limit  {history_len} "
    data = pd.read_sql(q, db.engine)

    ax = plt.gca()
    data.plot(kind='bar', x='date_shamsi', y='value', ax=ax, color='green')

    reshaped_text = \
        arabic_reshaper.reshape("ارزش معادلات کل")
    text = get_display(reshaped_text)
    ax.set_title(text)

    plt.savefig(f'../../output/reports/ارزش معادلات کل.png')
    ax.cla()

    return data


def histogram_value_grouped(history_len):
    print(pathlib.Path(__file__).parent.absolute())
    print(pathlib.Path().absolute())
    q = f"select date_shamsi,SUM(value) as value  from stock_price group by dtyyyymmdd order by date_shamsi desc limit  {history_len} "
    total = pd.read_sql(q, db.engine)

    codes = db.session.query(db.distinct(Stocks.group_code)).all()

    for i, code in enumerate(codes):
        print(code[0])
        q = f"""select date_shamsi,group_name,SUM(value) as value
                from(select * from stock_price Stock_price , stocks Stock where Stock.code = Stock_price.code) where group_code == {code[0]}
                group by dtyyyymmdd,group_code order by date_shamsi desc limit {history_len}
                """
        data = pd.read_sql(q, db.engine)
        result = pd.merge(total, data, on='date_shamsi')
        if len(result) != 0:
            result['ratio'] = (result.value_y / result.value_x) * 100
            ax = plt.gca()
            result.plot(kind='bar', x='date_shamsi', y='ratio', ax=ax, color='green')

            reshaped_text = \
                arabic_reshaper.reshape(result.group_name.iloc[0])
            text = get_display(reshaped_text)
            ax.set_title(text)

            plt.savefig(f'../../output/reports/{code[0]}.png')
            ax.cla()

    return None
