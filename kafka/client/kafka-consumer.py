#!/usr/bin/env python

from kafka import KafkaConsumer

topics=['test']
bootstrap_servers=['127.0.0.1:9094']
sasl_plain_username='admin'
sasl_plain_password='admin123'
# sasl_plain_username='user1'
# sasl_plain_password='password1'
# sasl_mechanism='PLAIN'
sasl_mechanism='SCRAM-SHA-256'
security_protocol='SASL_PLAINTEXT'
# consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest')
# api_version=(0,10)
api_version=None


# sasl.mechanism=SCRAM-SHA-256
# # Configure SASL_SSL if SSL encryption is enabled, otherwise configure SASL_PLAINTEXT
# security.protocol=SASL_SSL

# sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
#   username="kafkaclient1" \
#   password="kafkaclient1-secret";


consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,auto_offset_reset='earliest',
    sasl_plain_username=sasl_plain_username,sasl_plain_password=sasl_plain_password,sasl_mechanism=sasl_mechanism,security_protocol=security_protocol,
    api_version=api_version)
consumer.subscribe(topics)

print(consumer)

for msg in consumer:
    # print (msg)
    print (msg.value)












