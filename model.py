import uuid
import datetime
import json


class TransactionType:
    """
    list of transaction types
    """
    BUY = 'BUY'
    SELL = 'SELL'

class OrderValidity:
    """
    list of validity timespans for an order
    """
    DAY = 'DAY' # order is valid till the End of Day

class Order:
    """
    Order class stores relevant metadata of an order
    """
    def __init__(self, order_type, trader_id, instrument, price, quantity, validity=None, placed_at=str(datetime.datetime.now()), order_id=None):
        self.order_id = order_id if order_id else uuid.uuid4().hex
        self.order_type = order_type
        self.trader_id = trader_id
        self.instrument = instrument
        self.price = price
        self.quantity = quantity
        self.validity = validity
        self.placed_at = placed_at

    def __str__(self):
        return '''Order ID   : {}\nOrder Type : {}\nTrader ID  : {}\nInstrument : {}\nPrice      : {}\nQuantity   : {}\nValidity   : {}\nPlaced at  : {}\n\n'''.format(
            self.order_id, self.order_type, self.trader_id, self.instrument['instrument_name'], self.price, self.quantity, self.validity, self.placed_at)

    def __repr__(self):
        return '''Order ID   : {}\nOrder Type : {}\nTrader ID  : {}\nInstrument : {}\nPrice      : {}\nQuantity   : {}\nValidity   : {}\nPlaced at  : {}\n\n'''.format(
            self.order_id, self.order_type, self.trader_id, self.instrument['instrument_name'], self.price, self.quantity, self.validity, self.placed_at)
