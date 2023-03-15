from kafka import KafkaConsumer
from json import loads
import json
import copy
import pandas as pd
from model import Order, TransactionType
from exchange import Exchange

exchange = Exchange(instrument_list_path='instruments.csv')

consumer = KafkaConsumer(
    'exchange',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

buy_orders = []
sell_orders = []

trades = pd.DataFrame()

for message in consumer:
    message = message.value
    print('{}\n'.format(message))

    order = Order(
        order_id=message['order_id'], 
        order_type=message['order_type'], 
        trader_id=message['trader_id'], 
        instrument=message['instrument'], 
        price=message['price'], 
        quantity=message['quantity'], 
        validity=message['validity'], 
        placed_at=message['placed_at'])

    trade, buy_orders, sell_orders = exchange.match_maker(order, buy_orders, sell_orders)

    if trade:
        trade['timestamp'] = pd.to_datetime(trade['timestamp'])
        # save the trades
        trades = trades.append(trade, ignore_index=True)

        df = copy.deepcopy(trades)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        grouped = df.groupby('instrument').resample('5T').mean()

        print(grouped)

        sma = df['price'].rolling('5min').mean().tail(10)

        # Group the data by instrument and calculate the simple moving average with a 5-minute window for the last 10 minutes
        # sma = grouped.groupby('instrument')['price'].rolling('10min').mean().tail(10)

        print("Simple Moving Average : \n{}".format(sma))

    print('Trades completed :: {}'.format(trades.shape[0]))
    print('Total number of pending buy orders :: {}'.format(len(buy_orders)))
    print('Total number of pending sell orders :: {}'.format(len(sell_orders)))
    