#!/usr/bin/env python

from kafka import KafkaProducer
# from kafka.errors import KafkaError

topic = 'test'
bootstrap_servers = ['127.0.0.1:9094']





topics=['test']
bootstrap_servers=['127.0.0.1:9094']
# sasl_plain_username='admin'
# sasl_plain_password='admin123'
sasl_plain_username='user1'
sasl_plain_password='password1'
# sasl_mechanism='PLAIN'
sasl_mechanism='SCRAM-SHA-256'
security_protocol='SASL_PLAINTEXT'
# consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest')
# api_version=(0,10)
api_version=None

producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
    sasl_plain_username=sasl_plain_username,sasl_plain_password=sasl_plain_password,sasl_mechanism=sasl_mechanism,security_protocol=security_protocol,
    api_version=api_version)



# producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
# producer.subscribe(['test'])

print(producer)

for i in range(3):
    s = producer.send(topic, key=b'foo', value=b'var')
    print(s.get(timeout=3))














