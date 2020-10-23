#!/usr/bin/env python

from kafka import KafkaProducer
# from kafka.errors import KafkaError

topic = 'test'
bootstrap_servers = ['127.0.0.1:9094']

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
# producer.subscribe(['test'])

print(producer)

for i in range(3):
    s = producer.send(topic, key=b'foo', value=b'var')
    print(s.get(timeout=3))














