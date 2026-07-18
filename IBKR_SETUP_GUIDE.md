# IB Gateway Paper Trading 环境准备

使用 Interactive Brokers (IB) Paper Trading 环境进行 Python API 开发前的准备工作。

---

## 0. 申请ibkr模拟账号

---

## 1. 下载 IB Gateway / TWS

下载地址：

### IB Gateway

https://www.interactivebrokers.com/en/trading/ibgateway-latest.php?p=stable


### TWS (Trader Workstation)

https://www.interactivebrokers.com/cn/trading/download-tws.php?p=stable


后续开发过程中主要使用**IB Gateway**：

- **IB Gateway**：用于程序化交易 API 连接
- **TWS**：可用于查看订单、账户状态以及调试

---

# 2. 启动 IB Gateway

启动 IB Gateway 后：

1. 选择 **Paper Trading**
2. 使用 Paper Trading 账号登录

---

# 3. 开启 API

进入：

```
Configure → API → Settings
```

确认配置：

```
Read-Only API
```

需要保持 **未勾选**。

原因：

- 勾选 `Read-Only API` 时，API 只能查询数据
- 无法通过 Python API 创建、修改或取消订单


> 注意：
>
> 实际测试发现，部分情况下即使默认没有勾选 `Read-Only API`，API 下单仍可能失败。
>
> 如果遇到无法下单的问题，可以尝试：
>
> 1. 勾选 `Read-Only API`
> 2. 保存并重启 IB Gateway
> 3. 再取消勾选 `Read-Only API`
> 4. 保存并重新启动 IB Gateway


---

# 4. API 端口配置

IB Gateway Paper Trading 默认 API 端口：

```
4002
```

Python 连接配置：

```python
HOST = "127.0.0.1"
PORT = 4002
CLIENT_ID = 1
```

如果修改过 IB Gateway 的 API 端口，需要同步修改 Python 配置。

---

# 5. 安装 Python 依赖

安装 `ib_insync`：

```bash
pip install ib_insync
```

---

# 6. IB API 功能对应关系

通过 `ib_insync` 可以调用 IB API 完成常见交易功能。


## 6.1 查询账户信息

功能：

- 查询账户余额
- 查询净值
- 查询保证金
- 查询资金状态


API：

```python
ib.accountSummary()
```

示例：

```python
summary = ib.accountSummary()

for item in summary:
    print(
        item.tag,
        item.value,
        item.currency
    )
```


---

## 6.2 获取行情数据

功能：

- 查询股票实时价格
- 获取 Bid / Ask
- 获取历史 K 线数据


API：

### 实时行情

```python
ib.reqMktData()
```


示例：

```python
contract = Stock(
    "QQQ",
    "SMART",
    "USD"
)

ticker = ib.reqMktData(contract)

ib.sleep(2)

print(ticker.last)
```


### 历史行情

```python
ib.reqHistoricalData()
```

示例：

```python
bars = ib.reqHistoricalData(
    contract,
    durationStr="1 D",
    barSizeSetting="5 mins",
    whatToShow="TRADES"
)

for bar in bars:
    print(bar)
```

---

## 6.3 创建订单

功能：

- 市价单
- 限价单
- 止损单


API：

```python
ib.placeOrder()
```


示例：

```python
contract = Stock(
    "QQQ",
    "SMART",
    "USD"
)

order = MarketOrder(
    "BUY",
    1
)

trade = ib.placeOrder(
    contract,
    order
)
```


---

## 6.4 查询订单状态

功能：

- 查看订单是否提交
- 查看成交数量
- 查看剩余数量


API：

```python
ib.openTrades()
```


示例：

```python
trades = ib.openTrades()

for trade in trades:
    print(
        trade.order.orderId,
        trade.orderStatus.status,
        trade.orderStatus.filled
    )
```


常见订单状态：

| 状态 | 说明 |
|---|---|
| PendingSubmit | 已发送，等待 IB 处理 |
| PreSubmitted | IB 已收到 |
| Submitted | 已提交市场 |
| Filled | 已成交 |
| PendingCancel | 等待取消 |
| Cancelled | 已取消 |


---

## 6.5 取消订单

功能：

- 取消单个订单
- 取消所有未成交订单


API：

```python
ib.cancelOrder()
```


示例：

```python
for trade in ib.openTrades():
    ib.cancelOrder(
        trade.order
    )
```


取消所有订单：

```python
ib.reqGlobalCancel()
```


---

## 6.6 开发自动定投策略

功能：

- 定期买入 ETF
- 自动计算购买数量
- 自动提交订单
- 记录交易结果


常用 API：

| 功能 | API |
|---|---|
| 获取账户资金 | `ib.accountSummary()` |
| 获取当前价格 | `ib.reqMktData()` |
| 创建订单 | `ib.placeOrder()` |
| 查询订单状态 | `ib.openTrades()` |
| 查询持仓 | `ib.positions()` |
| 定时任务 | Python `schedule` / `asyncio` |


示例流程：

```
定时任务触发
        |
        v
查询账户资金
        |
        v
获取 QQQ 当前价格
        |
        v
计算购买数量
        |
        v
创建 BUY MarketOrder
        |
        v
提交订单
        |
        v
检查成交状态
```


---

# 7. 环境检查

开始运行 Python API 程序前，请确认：

- [x] IB Gateway 已启动
- [x] 已登录 Paper Trading
- [x] Read-Only API 未勾选
- [x] Python 已安装 `ib_insync`

完成以上配置后，即可通过 Python API 开发自动交易程序。