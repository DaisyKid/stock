from ib_insync import *
import sys


HOST = "127.0.0.1"
PORT = 4002
CLIENT_ID = 1


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


# 获取所有 open orders
open_orders = ib.openOrders()

print(f"Found {len(open_orders)} open orders")


for order in open_orders:
    print("Cancel:", order.orderId)
    ib.cancelOrder(order)


ib.sleep(2)


# 检查状态
print("\nCurrent open orders:")
for order in ib.openOrders():
    print(order.orderId)


ib.disconnect()