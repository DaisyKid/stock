import requests
import mysql.connector
from datetime import datetime

API_KEY = "15c4498a3d50495781dc4b0336dbc94a"

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pass",
    "database": "stock_db"
}


def fetch_latest(symbol):
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": "1day",
        "outputsize": 2,   # 只拿最近2天，防止节假日
        "apikey": API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "values" not in data:
        print("error:", symbol, data)
        return None

    # 最新一天（values是倒序）
    latest = data["values"][0]

    return latest


def save_to_mysql(symbol, row):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    sql = """
    INSERT INTO stock_daily_price
    (ticker, trade_date, open_price, high_price, low_price, close_price, volume)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        open_price=VALUES(open_price),
        high_price=VALUES(high_price),
        low_price=VALUES(low_price),
        close_price=VALUES(close_price),
        volume=VALUES(volume)
    """

    cursor.execute(sql, (
        symbol,
        row["datetime"],
        float(row["open"]),
        float(row["high"]),
        float(row["low"]),
        float(row["close"]),
        int(row.get("volume", 0))
    ))

    conn.commit()
    cursor.close()
    conn.close()

    print(symbol, "updated:", row["datetime"])


def update_all(symbols):
    for i, s in enumerate(symbols):

        try:
            row = fetch_latest(s)

            if row:
                save_to_mysql(s, row)

        except Exception as e:
            print("fail:", s, e)

        # 防止限流
        if i % 50 == 0:
            import time
            time.sleep(1)


if __name__ == "__main__":

    stocks = ["AAPL", "MSFT", "NVDA", "AMZN", "TSLA"]

    update_all(stocks)