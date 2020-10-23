#!/usr/bin/env python

from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers=['127.0.0.1:9094'],auto_offset_reset='earliest')
consumer.subscribe(['test'])

print(consumer)

for msg in consumer:
    # print (msg)
    print (msg.value)










