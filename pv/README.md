# PV

## OpenEBS

### Prerequisite
https://docs.openebs.io/docs/next/prerequisites.html

on target storage nodes
```
yum install iscsi-initiator-utils -y
sudo systemctl enable --now iscsid
```

```
[contrail@csn1 ~]$ cat /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.1994-05.com.redhat:5e96b7d4273k
[contrail@csn1 ~]$
```

enable SNAT for contrail
```
kubectl apply -f openebs/ip_fabric_snat.yml
```


### Install Openebs

```
kubectl create ns openebs
helm repo add openebs https://openebs.github.io/charts
helm repo update
helm install --namespace openebs openebs openebs/openebs --values openebs/values-contrail.yml 

NAME: openebs
LAST DEPLOYED: Fri Nov 20 15:15:57 2020
NAMESPACE: openebs
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The OpenEBS has been installed. Check its status by running:
$ kubectl get pods -n openebs

For dynamically creating OpenEBS Volumes, you can either create a new StorageClass or
use one of the default storage classes provided by OpenEBS.

Use `kubectl get sc` to see the list of installed OpenEBS StorageClasses. A sample
PVC spec using `openebs-jiva-default` StorageClass is given below:"

---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: demo-vol-claim
spec:
  storageClassName: openebs-jiva-default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5G
---

Please note that, OpenEBS uses iSCSI for connecting applications with the
OpenEBS Volumes and your nodes should have the iSCSI initiator installed.

For more information, visit our Slack at https://openebs.io/community or view the documentation online at http://docs.openebs.io/.

```

```
ckim-mbp:pv ckim$ kubectl get pod -n openebs

NAME                                           READY   STATUS    RESTARTS   AGE
maya-apiserver-6f5b6cb69d-26gt9                1/1     Running   0          11m
openebs-admission-server-754fd7bb56-6qnr2      1/1     Running   0          11m
openebs-localpv-provisioner-7bc9c57f67-vg7qm   1/1     Running   0          11m
openebs-ndm-524r6                              1/1     Running   0          11m
openebs-ndm-operator-6bd5d9dd77-6z6g7          1/1     Running   0          11m
openebs-provisioner-846bb46c7d-sdstz           1/1     Running   0          11m
openebs-snapshot-operator-5476bb8755-krg2v     2/2     Running   0          11m
ckim-mbp:pv ckim$ 
ckim-mbp:Downloads ckim$ kubectl get sc
NAME                        PROVISIONER                                                AGE
openebs-device              openebs.io/local                                           25m
openebs-hostpath            openebs.io/local                                           25m
openebs-jiva-default        openebs.io/provisioner-iscsi                               25m
openebs-snapshot-promoter   volumesnapshot.external-storage.k8s.io/snapshot-promoter   25m
ckim-mbp:Downloads ckim$
ckim-mbp:Downloads ckim$ kubectl label nodes csn1.pod3.cce node=openebs
node/csn1.pod3.cce labeled
```

## StorageClass openebs-device 

Attach block device(s) to the node.
```
[contrail@csn1 ~]$ lsblk
NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda               8:0    0  100G  0 disk
├─sda1            8:1    0    1G  0 part /boot
└─sda2            8:2    0   99G  0 part
  ├─centos-root 253:0    0   50G  0 lvm  /
  ├─centos-swap 253:1    0  7.9G  0 lvm
  └─centos-home 253:2    0 41.1G  0 lvm  /home
sdb               8:16   0    5G  0 disk
└─sdb1            8:17   0    5G  0 part
sdc               8:32   0    5G  0 disk
└─sdc1            8:33   0    5G  0 part
sdd               8:48   0    5G  0 disk
└─sdd1            8:49   0    5G  0 part
sr0              11:0    1 1024M  0 rom
[contrail@csn1 ~]$
[contrail@csn1 ~]$ sudo wipefs -f -a /dev/sdb1

```


Add PVC/POD
```
ckim-mbp:pv ckim$ kubectl apply -f local-device-pod.yaml 
persistentvolumeclaim/local-device-pvc-1 created
persistentvolumeclaim/local-device-pvc-2 created
pod/hello-local-device-pod-1 created
pod/hello-local-device-pod-2 created
ckim-mbp:pv ckim$ 
ckim-mbp:pv ckim$ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS     REASON   AGE
pvc-95e0095a-2bf5-11eb-862f-005056bb1686   5G         RWO            Delete           Bound    default/local-device-pvc-1   openebs-device            7m59s
pvc-98ff9aee-2bf5-11eb-862f-005056bb1686   5G         RWO            Delete           Bound    default/local-device-pvc-2   openebs-device            7m59s
ckim-mbp:pv ckim$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
dnsutils                   1/1     Running   237        9d
hello-local-device-pod-1   1/1     Running   0          8m10s
hello-local-device-pod-2   1/1     Running   0          8m10s
ckim-mbp:pv ckim$ kubectl get blockdevice
No resources found in default namespace.
ckim-mbp:pv ckim$ kubectl get blockdevice -A
NAMESPACE   NAME                                           NODENAME        SIZE           CLAIMSTATE   STATUS   AGE
openebs     blockdevice-0eb95d2e11d7811505f25c34331bedba   csn1.pod3.cce   5367643648     Claimed      Active   8m56s
openebs     blockdevice-3ed8f5913c01c89143f9534cf6dc105b   csn1.pod3.cce   5367643648     Unclaimed    Active   8m55s
openebs     blockdevice-ddae026b241e7ca61201ee8579c361f0   csn1.pod3.cce   5367643648     Claimed      Active   8m56s
openebs     blockdevice-f72f1f65c5e9a300a22df07d0431c891   csn1.pod3.cce   107373116928   Claimed      Active   61m
ckim-mbp:pv ckim$ 



[contrail@csn1 ~]$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0  100G  0 disk
├─sda1   8:1    0    1G  0 part /boot
└─sda2   8:2    0   99G  0 part
  ├─centos-root
       253:0    0   50G  0 lvm  /
  ├─centos-swap
       253:1    0  7.9G  0 lvm
  └─centos-home
       253:2    0 41.1G  0 lvm  /home
sdb      8:16   0    5G  0 disk
└─sdb1   8:17   0    5G  0 part /var/lib/kubelet/pods/9c20ed7f-2bf5-11eb-862f-005056bb1686/volumes/kubernetes.io~local-volume/pvc-95e0095
sdc      8:32   0    5G  0 disk
└─sdc1   8:33   0    5G  0 part /var/lib/kubelet/pods/9c451d76-2bf5-11eb-862f-005056bb1686/volumes/kubernetes.io~local-volume/pvc-98ff9ae
sdd      8:48   0    5G  0 disk
└─sdd1   8:49   0    5G  0 part
sr0     11:0    1 1024M  0 rom
[contrail@csn1 ~]$

```


## StorageClass openebs-hostpath


```
kubectl patch storageclass openebs-hostpath    -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```


```
ckim-mbp:pv ckim$ kubectl get pod
NAME                         READY   STATUS    RESTARTS   AGE
dnsutils                     1/1     Running   238        9d
hello-local-hostpath-pod-1   1/1     Running   0          37s
hello-local-hostpath-pod-2   1/1     Running   0          37s
ckim-mbp:pv ckim$ 
ckim-mbp:pv ckim$ 
ckim-mbp:pv ckim$ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                          STORAGECLASS       REASON   AGE
pvc-355cad56-2bf8-11eb-862f-005056bb1686   5G         RWO            Delete           Bound    default/local-hostpath-pvc     openebs-hostpath            8m14s
pvc-3f117214-2bf9-11eb-862f-005056bb1686   5G         RWO            Delete           Bound    default/local-hostpath-pvc-1   openebs-hostpath            68s
pvc-4233ae55-2bf9-11eb-862f-005056bb1686   5G         RWO            Delete           Bound    default/local-hostpath-pvc-2   openebs-hostpath            68s
ckim-mbp:pv ckim$ kubectl get pod
NAME                         READY   STATUS    RESTARTS   AGE
dnsutils                     1/1     Running   238        9d
hello-local-hostpath-pod-1   1/1     Running   0          79s
hello-local-hostpath-pod-2   1/1     Running   0          79s
ckim-mbp:pv ckim$ kubectl exec hello-local-hostpath-pod-1 -- df -h /mnt/store
Filesystem                Size      Used Available Use% Mounted on
/dev/mapper/centos-root
                         50.0G      7.9G     42.1G  16% /mnt/store
ckim-mbp:pv ckim$ 


[contrail@csn1 ~]$ df -h /var/openebs/local/
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/centos-root   50G  8.0G   43G  16% /
[contrail@csn1 ~]$
[contrail@csn1 ~]$ ll /var/openebs/local/
total 0
drwxrwxrwx. 2 root root 23 Nov 21 07:51 pvc-355cad56-2bf8-11eb-862f-005056bb1686
drwxrwxrwx. 2 root root 23 Nov 21 07:58 pvc-3f117214-2bf9-11eb-862f-005056bb1686
drwxrwxrwx. 2 root root 23 Nov 21 07:58 pvc-4233ae55-2bf9-11eb-862f-005056bb1686
[contrail@csn1 ~]$ cat /var/openebs/local/pvc-355cad56-2bf8-11eb-862f-005056bb1686/greet.txt
Sat Nov 21 12:51:47 UTC 2020 [hello-local-hostpath-pod] Hello from OpenEBS Local PV.
Sat Nov 21 12:55:12 UTC 2020 [hello-local-hostpath-pod-2] Hello from OpenEBS Local PV.
Sat Nov 21 12:55:14 UTC 2020 [hello-local-hostpath-pod-1] Hello from OpenEBS Local PV.
[contrail@csn1 ~]$ cat /var/openebs/local/pvc-3f117214-2bf9-11eb-862f-005056bb1686/greet.txt
Sat Nov 21 12:58:53 UTC 2020 [hello-local-hostpath-pod-1] Hello from OpenEBS Local PV.
[contrail@csn1 ~]$ cat /var/openebs/local/pvc-4233ae55-2bf9-11eb-862f-005056bb1686/greet.txt
Sat Nov 21 12:58:55 UTC 2020 [hello-local-hostpath-pod-2] Hello from OpenEBS Local PV.
[contrail@csn1 ~]$

```







## register docker login 

```
docker login -u kimcharli -p xxxxxxxx
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=/Users/ckim/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson
```







