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
        self.eod_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
        self.instruments = pd.read_csv(instrument_list_path).to_dict('records')
           
    def place_order(self, order_type, trader_id, instrument, price, quantity, validity):
        order = Order(order_type=order_type, trader_id=trader_id, 
            instrument=instrument, price=price, quantity=quantity, validity=validity)
        
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:dumps(x).encode('utf-8'))

        producer.send('exchange', value=order.__dict__)

        print('Order placed : \n{}'.format(order))

        return order.order_id

    def match_maker(self, order, buy_orders, sell_orders):

        if order.order_type == TransactionType.BUY:
            # call function here
            trade_settled = self.algorithm(order, buy_orders, sell_orders)

            # when current order is not settled,  its added in buy orders list
            if not trade_settled:
                buy_orders.append(order)

        elif order.order_type == TransactionType.SELL:
            # call function here
            trade_settled = self.algorithm(order, buy_orders, sell_orders)

            # when current order is not settled,  its added in sell orders list
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

    def algorithm(self, order, buy_orders, sell_orders):
        current_instruments_orders = self.get_current_instruments_orders(order, buy_orders, sell_orders)

        if order.order_type == TransactionType.BUY:
            current_type_orders = buy_orders
            opposite_orders = sell_orders
        elif order.order_type == TransactionType.SELL:
            current_type_orders = sell_orders
            opposite_orders = buy_orders

        trade_settled = False
        # check against all SELL orders of this orders instrument
        for existing_order in current_instruments_orders:
            # Checking conditions :: 
            # expected sell price is less than the current orders price
            # BUY and SELL orders are of different trader
            if (order.price >= existing_order.price) and (order.trader_id != existing_order.trader_id):
                quantity_traded = min(order.quantity, existing_order.quantity)
                if (quantity_traded == order.quantity) and (quantity_traded == existing_order.quantity):
                    # dont add order
                    # remove opposite order
                    opposite_orders.remove(existing_order)
                else:
                    if quantity_traded < order.quantity:
                        # add this order with reduced quantity
                        order.quantity = order.quantity - quantity_traded
                        current_type_orders.append(order)

                    if quantity_traded < existing_order.quantity:
                        # dont add order
                        # remove that much from order
                        existing_order.quantity = existing_order.quantity - quantity_traded
                trade_settled = True

                if order.order_type == TransactionType.BUY:
                    trade = {
                        'BUY_ORDER' : order.order_id,
                        'SELL_ORDER' : existing_order.order_id,
                        'PRICE' : existing_order.price,
                        'SETTLED QUANTITY' : quantity_traded,
                        'INSTRUMENT' : order.instrument['instrument_name']
                        }
                elif order.order_type == TransactionType.SELL:
                    trade = {
                        'BUY_ORDER' : existing_order.order_id,
                        'SELL_ORDER' : order.order_id,
                        'PRICE' : order.price,
                        'SETTLED QUANTITY' : quantity_traded,
                        'INSTRUMENT' : order.instrument['instrument_name']
                    }
                print('Trade Settled :: \n{}'.format(trade))
                break
        return trade_settled