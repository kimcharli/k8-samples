# k8-samples

To collect the examples to use

## metallb
```
kubectl apply -f metallb/ns.yml 
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.4/manifests/metallb.yaml
```

Start a service
```
kubectl apply -f svc/nginx-lb.yml 
```

```
ckim-mbp:k8-samples ckim$ kubectl get svc nginx
NAME    TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
nginx   LoadBalancer   10.98.63.199   127.0.0.240   9999:32040/TCP   37s
ckim-mbp:k8-samples ckim$ 
ckim-mbp:k8-samples ckim$ curl 127.0.0.1:9999
```


## kafka
Without metallb

```
helm install kafka bitnami/kafka --values kafka/values.yaml 
```

Test
```
kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:2.6.0-debian-10-r30 --namespace default --command -- sleep infinity
kubectl exec --tty -i kafka-client --namespace default -- bash

kafka-console-producer.sh \
    --broker-list kafka-0.kafka-headless.default.svc.cluster.local:9092 \
    --topic test

kafka-console-consumer.sh \
    --bootstrap-server kafka.default.svc.cluster.local:9092 \
    --topic test \
    --from-beginning
```


```
 kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:admin --allow-principal User:user-1 --operation read --operation write --topic finance-topic test

 I have no name!@kafka-0:/$ kafka-acls.sh --authorizer kafka.security.auth.SimpleAclAuthorizer --authorizer-properties zookeeper.connect=10.103.58.49:2181 --list --topic test
I have no name!@kafka-0:/$ 
 have no name!@kafka-0:/$ kafka-acls.sh --authorizer kafka.security.auth.SimpleAclAuthorizer --authorizer-properties zookeeper.connect=10.103.58.49:2181 --add --allow-principal User:admin --operation All --topic *
Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=bin, patternType=LITERAL)`: 
        (principal=User:admin, host=*, operation=ALL, permissionType=ALLOW) 

Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=bin, patternType=LITERAL)`: 
        (principal=User:admin, host=*, operation=ALL, permissionType=ALLOW) 

I have no name!@kafka-0:/$ kafka-acls.sh --authorizer kafka.security.auth.SimpleAclAuthorizer --authorizer-properties zookeeper.connect=10.103.58.49:2181 --add --allow-principal User:user1 --operation All --topic test
Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=test, patternType=LITERAL)`: 
        (principal=User:user1, host=*, operation=ALL, permissionType=ALLOW) 

Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=test, patternType=LITERAL)`: 
        (principal=User:user1, host=*, operation=ALL, permissionType=ALLOW) 

I have no name!@kafka-0:/$ kafka-acls.sh --authorizer kafka.security.auth.SimpleAclAuthorizer --authorizer-properties zookeeper.connect=10.103.58.49:2181 --list --topic testCurrent ACLs for resource `ResourcePattern(resourceType=TOPIC, name=test, patternType=LITERAL)`: 
        (principal=User:user1, host=*, operation=ALL, permissionType=ALLOW) 

I have no name!@kafka-0:/$ 
I have no name!@kafka-0:/$ kafka-configs.sh --zookeeper 10.103.58.49:2181 --alter --add-config 'SCRAM-SHA-256=[password=admin123],SCRAM-SHA-512=[password=admin123]' --entity-type users --entity-name admin
Warning: --zookeeper is deprecated and will be removed in a future version of Kafka.
Use --bootstrap-server instead to specify a broker to connect to.
Completed updating config for entity: user-principal 'admin'.
I have no name!@kafka-0:/$ 
I have no name!@kafka-0:/$ kafka-configs.sh --zookeeper 10.103.58.49:2181 --describe --entity-name admin --entity-type users 
Warning: --zookeeper is deprecated and will be removed in a future version of Kafka.
Use --bootstrap-server instead to specify a broker to connect to.
Configs for user-principal 'admin' are SCRAM-SHA-512=salt=MWxyejJsanN2cmRsOWhucGhtdDFldDllNzA=,stored_key=gAMgHwGboOrN+0JVkmfixm8WA/SHO4OxU7e22gqNwkXJ4zgAPa0aSa/MdTV3V/hoInr6jDJfBRiFppRRx1Swvg==,server_key=uLJ9UnIbiaNXsZ5Li7aHBkI/nOVME2hBOkewBuRxuXcsb6+Iu8hUN2o3Us4CsKEJ1FCcRyLQ4uRdeGvZ3obIwg==,iterations=4096,SCRAM-SHA-256=salt=anh3NjhhaHVqeGR0c3drcjJ5eWdxOHZ0OQ==,stored_key=oC6OmjQny/RN/+Vz4PAWA/37dok6zhNkxwBAal2k2nY=,server_key=qabebGzd+x9bYDreISKAWbI+/mKwdRDPs14ApA3PCCw=,iterations=4096
I have no name!@kafka-0:/$ 
I have no name!@kafka-0:/$ 


(kafka-python) ckim-mbp:k8-samples ckim$ kafka-configs.sh --zookeeper 10.103.58.49:2181 --alter --add-config 'SCRAM-SHA-256=[password=password1],SCRAM-SHA-512=[password=password1]' --entity-type users --entity-name user1
bash: kafka-configs.sh: command not found
(kafka-python) ckim-mbp:k8-samples ckim$ 
(kafka-python) ckim-mbp:k8-samples ckim$ k exec -it kafka-0 -- bashI have no name!@kafka-0:/$ kafka-configs.sh --zookeeper 10.103.58.49:2181 --alter --add-config 'SCRAM-SHA-256=[password=password1],SCRAM-SHA-512=[password=password1]' --entity-type users --entity-name user1
Warning: --zookeeper is deprecated and will be removed in a future version of Kafka.
Use --bootstrap-server instead to specify a broker to connect to.
Completed updating config for entity: user-principal 'user1'.
I have no name!@kafka-0:/$ kafka-configs.sh --zookeeper 10.103.58.49:2181 --describe --entity-name user1 --entity-type users
Warning: --zookeeper is deprecated and will be removed in a future version of Kafka.
Use --bootstrap-server instead to specify a broker to connect to.
Configs for user-principal 'user1' are SCRAM-SHA-512=salt=MWV6Z2t4c2J0em10anJjejdqbTRtcmpsdGc=,stored_key=90rq1h9dfvzyAHvFi5zTdDeLHdzZnCTguff+ZwwuaQ6LrQvdGLBxBuqbKk0p+4gqDUrFW2K3My5630qEylNGrw==,server_key=ig6DfQePNd5FTgIaGQwZA0JxJj8Saeph/+hX8tRsSuMa8MA1g21F9CQtO1U6RTaw4dFXjLbZ8j4DzgVtLMrHxQ==,iterations=4096,SCRAM-SHA-256=salt=bWJmMHdtbWxteGNpcGZiNng0cGdjd2R3dg==,stored_key=MFecbAOEog2ZYKtSal/Vp6YruK1tJIoO6jRrByqsjJI=,server_key=ne5uRq2BA+trmjTTH02rOinoDYiaqLgQvNfWLKP4QGM=,iterations=4096
I have no name!@kafka-0:/$ 

```


```
I have no name!@kafka-0:/$ zookeeper-shell.sh 10.103.58.49:2181 ls /path
Connecting to 10.103.58.49:2181

WATCHER::

WatchedEvent state:SyncConnected type:None path:null

WATCHER::

WatchedEvent state:SaslAuthenticated type:None path:null
Node does not exist: /path
I have no name!@kafka-0:/$ 
I have no name!@kafka-0:/$ cat /opt/bitnami/kafka/config/kafka_jaas.conf 
KafkaClient {
   org.apache.kafka.common.security.plain.PlainLoginModule required
   username="admin"
   password="PDUZQ60f9T";
   };
KafkaServer {
   org.apache.kafka.common.security.plain.PlainLoginModule required
   user_admin="PDUZQ60f9T"
   user_user1="d4fJxT8O8L"
   user_user2="Qmx2aQ7JU0";
   org.apache.kafka.common.security.scram.ScramLoginModule required;
   };
Client {
   org.apache.kafka.common.security.plain.PlainLoginModule required
   username="zoo-user-1"
   password="zoo-pass-1";
   };
I have no name!@kafka-0:/$ 

I have no name!@kafka-0:/$ kafka-topics.sh --zookeeper=10.103.58.49:2181 --list
__consumer_offsets
test
I have no name!@kafka-0:/$ 
I have no name!@kafka-0:/$ kafka-topics.sh --zookeeper=10.103.58.49:2181 --describe test
Topic: __consumer_offsets       PartitionCount: 50      ReplicationFactor: 1    Configs: compression.type=producer,cleanup.policy=compact,segment.bytes=104857600


```



