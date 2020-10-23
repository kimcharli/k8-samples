#!/usr/bin/env python

from kafka import KafkaConsumer

topics=['test']
bootstrap_servers=['127.0.0.1:9094']
# sasl_plain_username='admin'
# sasl_plain_password='admin123'
sasl_plain_username='user1'
sasl_plain_password='password1'
sasl_mechanism='PLAIN'
security_protocol='SASL_PLAINTEXT'
# consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest')

consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest',
    sasl_plain_username=sasl_plain_username,sasl_plain_password=sasl_plain_password,sasl_mechanism=sasl_mechanism,security_protocol=security_protocol)
consumer.subscribe(topics)

print(consumer)

for msg in consumer:
    # print (msg)
    print (msg.value)












