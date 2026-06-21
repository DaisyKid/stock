# 📈 Stock Data Pipeline（Stooq + Twelve Data + MySQL）

构建一个本地美股历史 + 每日更新数据库系统

---
# 0. 运行环境
python3.11

```
conda create -n stock python=3.11
conda activate stock
pip install mysql-connector-python
```

# 1. MySQL 表设计
```
CREATE DATABASE IF NOT EXISTS stock_db;
USE stock_db;

CREATE TABLE IF NOT EXISTS stock_daily_price (
    ticker VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,

    open_price DECIMAL(10,4),
    high_price DECIMAL(10,4),
    low_price DECIMAL(10,4),
    close_price DECIMAL(10,4),

    volume BIGINT,

    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (ticker, trade_date)
);
```

example:
```
mysql> SELECT * FROM stock_daily_price;
+--------+------------+------------+------------+-----------+-------------+-----------+---------------------+
| ticker | trade_date | open_price | high_price | low_price | close_price | volume    | created_time        |
+--------+------------+------------+------------+-----------+-------------+-----------+---------------------+
| AAPL   | 2026-06-18 |   298.1100 |   300.5700 |  295.6200 |    298.0100 |  85962200 | 2026-06-21 21:36:53 |
| AMZN   | 2026-06-18 |   240.1200 |   245.7300 |  236.0200 |    244.3900 |  75624400 | 2026-06-21 21:36:58 |
| MSFT   | 2026-06-18 |   377.8200 |   381.3700 |  373.2800 |    379.4000 |  59714200 | 2026-06-21 21:36:55 |
| NVDA   | 2026-06-18 |   207.3300 |   211.3900 |  206.5000 |    210.6900 | 241272000 | 2026-06-21 21:36:56 |
| TSLA   | 2026-06-18 |   398.1000 |   402.5200 |  384.7000 |    400.4900 |  58384700 | 2026-06-21 21:36:59 |
+--------+------------+------------+------------+-----------+-------------+-----------+---------------------+
5 rows in set (0.02 sec)
```

# 2. 历史数据获取
https://stooq.com/db/h/


# 3. 历史数据存到 MySQL


# 4. Twelve Data API（日线）


接口：
```
https://api.twelvedata.com/time_series
```

# 5. Python 每日增量拉取 + 写 MySQL

# 6. 定时任务执行update.py


