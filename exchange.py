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
        
        
    def place_order(self, order_type, trader_id, instrument, quantity, validity):
        order = Order(order_type=order_type, trader_id=trader_id, 
            instrument=instrument, quantity=quantity, validity=validity)
        
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:dumps(x).encode('utf-8'))

        producer.send('exchange', value=order.__dict__)

        print('Order placed : {}'.format(order.order_id))

        return order.order_id


    def match_maker(self, order):
        pass
