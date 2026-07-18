from ib_insync import *
import math
import sys
import time


# ==================================================
# Configuration
# ==================================================

HOST = "127.0.0.1"

# IB Gateway Paper Trading
PORT = 4002

CLIENT_ID = 1


SYMBOL = "QQQ"
EXCHANGE = "SMART"
CURRENCY = "USD"


# 每次投入金额
INVEST_AMOUNT = 1000.0



# ==================================================
# Connect IB Gateway
# ==================================================

ib = IB()


try:
    ib.connect(
        HOST,
        PORT,
        clientId=CLIENT_ID,
        timeout=10
    )

except Exception as e:
    print("IB Gateway connection failed:")
    print(e)
    sys.exit(1)



print("=" * 60)

print(
    "Connected:",
    ib.isConnected()
)


# ==================================================
# Account
# ==================================================

accounts = ib.managedAccounts()


if not accounts:
    print("No account found")
    ib.disconnect()
    sys.exit(1)


account = accounts[0]


print(
    "Account:",
    account
)


print("=" * 60)



# ==================================================
# Account Information
# ==================================================

print("\nAccount Information")


for v in ib.accountValues():

    if v.tag in [
        "NetLiquidation",
        "CashBalance",
        "BuyingPower"
    ]:

        print(
            f"{v.tag:<20} {v.value}"
        )



# ==================================================
# Create Contract
# ==================================================

contract = Stock(
    SYMBOL,
    EXCHANGE,
    CURRENCY
)


contracts = ib.qualifyContracts(contract)


if not contracts:

    print("Contract qualification failed")

    ib.disconnect()
    sys.exit(1)


print("\nContract Qualified")

print(contract)



# ==================================================
# Market Data
# ==================================================

print("\nRequest market data")


# 1 = realtime
# 3 = delayed
ib.reqMarketDataType(3)


ticker = ib.reqMktData(
    contract,
    "",
    False,
    False
)


# wait data
for i in range(10):

    ib.sleep(1)

    price = ticker.marketPrice()

    if price and not math.isnan(price):

        break


ib.cancelMktData(contract)



if (
    price is None
    or math.isnan(price)
    or price <= 0
):

    print(
        "Cannot get QQQ price"
    )

    ib.disconnect()
    sys.exit(1)



print(
    f"\nQQQ Price: ${price:.2f}"
)



# ==================================================
# Calculate Shares
# ==================================================

shares = math.floor(
    INVEST_AMOUNT / price
)


if shares <= 0:

    print(
        "Investment amount too small"
    )

    ib.disconnect()
    sys.exit(1)



cost = shares * price


print(
    f"Investment : ${INVEST_AMOUNT}"
)

print(
    f"Buy Shares : {shares}"
)

print(
    f"Estimated Cost : ${cost:.2f}"
)



# ==================================================
# Create Order
# ==================================================

# order = MarketOrder(
#     action="BUY",
#     totalQuantity=shares
# )

order = LimitOrder(
    "BUY",
    shares,
    694.00
)

order.tif = "DAY"
order.account = account



# ==================================================
# Submit Order
# ==================================================

print("\nSubmitting order...")


trade = ib.placeOrder(
    contract,
    order
)



# wait order update

print("\nWaiting order status...")


timeout = 10
start = time.time()


while not trade.isDone():

    ib.waitOnUpdate(timeout=1)

    status = trade.orderStatus.status

    print(
        "Order Status:",
        status
    )


    if time.time() - start > timeout:

        print(
            "Order timeout"
        )

        # ib.cancelOrder(order)

        break


print("\n========== ORDER RESULT ==========")


print(
    "Status:",
    trade.orderStatus.status
)



if trade.fills:

    fill = trade.fills[-1]


    print(
        "Filled Shares:",
        fill.execution.shares
    )


    print(
        "Fill Price:",
        fill.execution.price
    )


    print(
        "Execution Time:",
        fill.execution.time
    )


else:

    print(
        "No fill information"
    )



print(
    "================================="
)



# ==================================================
# Positions
# ==================================================

print("\nCurrent Positions")


positions = ib.positions()


if not positions:

    print(
        "No positions"
    )


else:

    for p in positions:


        print(
            f"{p.contract.symbol:<6}"
            f"{p.position:<10}"
            f"AvgCost={p.avgCost:.2f}"
        )



# ==================================================
# Open Orders
# ==================================================

print("\nOpen Orders")


orders = ib.openOrders()


if not orders:

    print(
        "No open orders"
    )

else:

    for o in orders:

        print(o)



# ==================================================
# Disconnect
# ==================================================

ib.disconnect()


print(
    "\nDisconnected"
)