import tehran_stocks.config as db
import matplotlib.pyplot as plt
from tehran_stocks import Stocks
import pandas as pd
import matplotlib.ticker as mtick

def histogram_value(history_len=31):
    q = f"select date_shamsi,SUM(value) as value  from stock_price group by dtyyyymmdd order by date_shamsi desc limit  {history_len} "
    data = pd.read_sql(q, db.engine)

    ax = plt.gca()
    data.plot(kind='bar', x='date_shamsi', y='value', ax=ax,color='green')

    plt.show()

    return data


def histogram_value_grouped():
    q = f'select count(distinct group_code) from stocks'
    number_of_group = pd.read_sql(q,db.engine).iloc[0][0]

    q = f"""select date_shamsi,group_name,SUM(value) as value
            from(select * from stock_price Stock_price , stocks Stock where Stock.code = Stock_price.code)
            group by dtyyyymmdd,group_code order by date_shamsi desc limit {number_of_group * 31}
            """
    data = pd.read_sql(q, db.engine)

    data.groupby(['date_shamsi', 'group_name']).size().groupby(level=0).apply(
        lambda x: 100 * x / x.sum()
    ).unstack().plot(kind='bar', stacked=True)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.show()

    return data
