import pandas as pd
import json
import datetime
from kafka import KafkaProducer
from json import dumps, loads
from model import TransactionType, OrderValidity, Order


class Exchange:
    """
    Exchange class, exposes place_order, match_maker, moving average and prodit calculations
    """

    transaction_type = TransactionType
    validity = OrderValidity


    def __init__(self, instrument_list_path):
        now = datetime.datetime.now()
        self.eod_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
        self.instruments = pd.read_csv(instrument_list_path).to_dict('records')
           
    def place_order(self, order_type, trader_id, instrument, price, quantity, validity):
        order = Order(order_type=order_type, trader_id=trader_id, 
            instrument=instrument, price=price, quantity=quantity, validity=validity)
        
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:dumps(x).encode('utf-8'))

        producer.send('exchange', value=order.__dict__)

        print('Order placed : {}'.format(order))

        return order.order_id

    def match_maker(self, order, buy_orders, sell_orders):

        if order.order_type == TransactionType.BUY:

            current_instruments_orders = self.get_current_instruments_orders(order, buy_orders, sell_orders)

            trade_settled = False
            # check against all SELL orders of this orders instrument
            for sell_order in current_instruments_orders:
                # Checking conditions :: 
                # expected sell price is less than the current orders price
                # BUY and SELL orders are of different trader
                if (order.price >= sell_order.price) and (order.trader_id != sell_order.trader_id):
                    trade = {
                        'BUY_ORDER' : order.order_id,
                        'SELL_ORDER' : sell_order.order_id,
                        'PRICE' : sell_order.price,
                        'INSTRUMENT' : order.instrument['instrument_name']
                    }
                    # when current order settles a trade, remove it from sell orders list
                    sell_orders.remove(sell_order)
                    print('Trade Settled :: \n{}'.format(trade))
                    trade_settled = True
                    break

            # when current order is not settled,  its added in buy orders list
            if not trade_settled:
                buy_orders.append(order)

        elif order.order_type == TransactionType.SELL:

            current_instruments_orders = self.get_current_instruments_orders(order, buy_orders, sell_orders)

            trade_settled = False
            # check against all BUY orders of this orders instrument
            for buy_order in current_instruments_orders:
                if (buy_order.price <= order.price) and (buy_order.trader_id != order.trader_id):
                    trade = {
                        'BUY_ORDER' : buy_order.order_id,
                        'SELL_ORDER' : order.order_id,
                        'PRICE' : order.price,
                        'INSTRUMENT' : order.instrument['instrument_name']
                    }
                    buy_orders.remove(buy_order)
                    print('Trade Settled :: \n{}'.format(trade))
                    trade_settled = True
                    break

            if not trade_settled:
                sell_orders.append(order)

        return buy_orders, sell_orders
        
    def get_current_instruments_orders(self, order, buy_orders, sell_orders):
        current_instruments_orders = []
        # if current order is BUY order, get list of SELL orders for same instrument
        if order.order_type == TransactionType.BUY:
            for s_order in sell_orders:
                if s_order.instrument['instrument_id'] == order.instrument['instrument_id']:
                    current_instruments_orders.append(s_order)
        # if current order is SELL order, get list of BUY orders for same instrument
        elif order.order_type == TransactionType.SELL:
            for s_order in buy_orders:
                if s_order.instrument['instrument_id'] == order.instrument['instrument_id']:
                    current_instruments_orders.append(s_order)
        print('Total opposite orders for this instrument : {}'.format(len(current_instruments_orders)))
        return current_instruments_orders 


