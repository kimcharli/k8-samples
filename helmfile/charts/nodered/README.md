# node-red

## start

```
helm install nodered .

```

## stop

```
helm delete nodered
```

## build

```
bash-5.0$ cat package.json
bash-5.0$ cat /data/settings.js
bash-5.0$ cat /data/flows.json



contrail@k3s:~$ sudo mkdir /var/nodered
contrail@k3s:~$ cd /var/nodered/
contrail@k3s:/var/nodered$ curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
contrail@k3s:/var/nodered$ sudo apt-get install -y nodejs

contrail@k3s:/var/nodered$ sudo vi package.json
contrail@k3s:/var/nodered$ sudo npm install --unsafe-perm --no-update-notifier --no-fund --only=prod
ckim@ckim-mbp ~ % sudo vi settings.js
contrail@k3s:/var/nodered$ sudo vi flows.json
contrail@k3s:/var/nodered$ sudo npm install node-red-node-feedparser

contrail@k3s:/var/nodered$ sudo chmod -R +w .

```

## TODO

- NODE_RED_CREDENTIAL_SECRET


