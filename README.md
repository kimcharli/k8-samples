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



