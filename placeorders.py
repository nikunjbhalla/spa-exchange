from exchange import Exchange
import random
import time

exchange = Exchange(instrument_list_path='instruments.csv')

instruments = exchange.instruments

n = 0
while n < 100:    
    exchange.place_order(
        order_type=random.choice([exchange.transaction_type.BUY, exchange.transaction_type.SELL]), 
        trader_id=random.choice([1,2,3,4]), 
        instrument=random.choice([instruments[0], instruments[1]]), 
        price=random.choice([10,20,30,40]), 
        quantity=random.choice([10,20,30,40]), 
        validity=exchange.validity.DAY)
    n = n + 1
    time.sleep(random.choice([1,2,3,4]))

# exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[0], price=10, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[0], price=12, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[0], price=8, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[1], price=200, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[1], price=200, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[1], price=200, quantity=10, validity=exchange.validity.DAY)

# exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[0], price=8, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[0], price=8, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[0], price=8, quantity=10, validity=exchange.validity.DAY)1
# exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[1], price=200, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[1], price=200, quantity=10, validity=exchange.validity.DAY)
# exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[1], price=200, quantity=10, validity=exchange.validity.DAY)