# Class Description
- createorders.py -> Calls the functions for exchange.py to create orders and add them to kafka 

- consumer.py -> Kafka consumer that accumulates all orders

- exchange.py -> Exchange class that has order create method that acts as kafka producer

- model.py -> Consists of model classes

## Completed
- transaction_type = BUY, SELL - Class created
- validity = DAY - Class created
- get_intruments() - Done
- place_order(instrument, transaction_type, quantity, validity) -> Print Order Details - Done

## Pending
- match_maker(order) -> check order with this instrument -> if matched output both orders matched/ check validity
- simple_moving_average
- calculate_profits
