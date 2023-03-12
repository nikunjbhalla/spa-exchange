from kafka import KafkaConsumer
from json import loads
import json
from model import Order

consumer = KafkaConsumer(
    'exchange',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

orders = []

for message in consumer:
    message = message.value
    print('Message :: {}'.format(message))

    order = Order(order_type=message['order_type'], 
            trader_id=message['trader_id'], 
            instrument=message['instrument'], 
            quantity=message['quantity'], 
            validity=message['validity'],
            placed_at=message['placed_at'])

    orders.append(order)

    print('Total number of orders :: {}'.format(len(orders)))
    
    