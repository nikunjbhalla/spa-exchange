from enum import Enum
import uuid
import pandas as pd
import datetime

class TransactionType(Enum):
    """
    Enum with list of transaction types
    """
    BUY = 'BUY'
    SELL = 'SELL'

class OrderValidity(Enum):
    """
    Enum with list of validity timespans for an order
    """
    DAY = 'DAY' # order is valid till the End of Day

class Order:
    """
    Order class stores relevant metadata of an order
    """
    def __init__(self, order_type, trader_id, instrument, quantity, validity=None):
        self.order_id = uuid.uuid4().hex
        self.order_type = order_type
        self.trader_id = trader_id
        self.instrument = instrument
        self.quantity = quantity
        self.validity = validity
        self.placed_at = datetime.datetime.now()

    def __str__(self):
        return '''Order ID   : {}\nOrder Type : {}\nTrader ID  : {}\nInstrument : {}\nQuantity   : {}\nValidity   : {}\nPlaced at  : {}\n\n'''.format(
            self.order_id, self.order_type.value, self.trader_id, self.instrument['instrument_name'], self.quantity, self.validity.value, self.placed_at)

    def __repr__(self):
        return '''Order ID   : {}\nOrder Type : {}\nTrader ID  : {}\nInstrument : {}\nQuantity   : {}\nValidity   : {}\nPlaced at  : {}\n\n'''.format(
            self.order_id, self.order_type.value, self.trader_id, self.instrument['instrument_name'], self.quantity, self.validity.value, self.placed_at)

class Exchange:
    """
    Exchange class, exposes place_order, match_maker, moving average and prodit calculations
    """

    transaction_type = TransactionType
    validity = OrderValidity

    def __init__(self, instrument_list_path):
        self.orders_list = []
        now = datetime.datetime.now()
        self.eod_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
        self.instruments = pd.read_csv(instrument_list_path).to_dict('records')

    def place_order(self, tx_type, trader_id, instrument, quantity, validity):
        order = Order(order_type=tx_type, trader_id=trader_id, 
            instrument=instrument, quantity=quantity, validity=validity) 
        print(order)
        self.orders_list.append(order) # write data to a kafka topic
        return order.order_id

    def orders(self):
        return self.orders_list # get data from kafka topic

    def match_maker(self, order):
        pass
