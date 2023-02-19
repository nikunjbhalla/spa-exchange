from exchange import Exchange

exchange = Exchange(instrument_list_path='instruments.csv')

instruments = exchange.instruments

exchange.place_order(
    exchange.transaction_type.BUY, 
    trader_id=1, instrument=instruments[0], 
    quantity=1, validity=exchange.validity.DAY)

exchange.place_order(
    exchange.transaction_type.SELL, 
    trader_id=2, instrument=instruments[0], 
    quantity=4, validity=exchange.validity.DAY)
