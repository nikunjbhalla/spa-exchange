from exchange import Exchange

exchange = Exchange(instrument_list_path='instruments.csv')

instruments = exchange.instruments

exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[0], price=100, quantity=5, validity=exchange.validity.DAY)
exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=2, instrument=instruments[1], price=250, quantity=5, validity=exchange.validity.DAY)
exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=1, instrument=instruments[0], price=80, quantity=5, validity=exchange.validity.DAY)
exchange.place_order(order_type=exchange.transaction_type.BUY, trader_id=2, instrument=instruments[1], price=220, quantity=5, validity=exchange.validity.DAY)

exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[0], price=100, quantity=5, validity=exchange.validity.DAY)
exchange.place_order(order_type=exchange.transaction_type.SELL, trader_id=3, instrument=instruments[1], price=230, quantity=5, validity=exchange.validity.DAY)
