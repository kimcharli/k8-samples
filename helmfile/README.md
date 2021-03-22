#

## setup argo-cd

```
mkdir -p charts/argo-cd
create charts/argo-cd/Chart.yaml
create charts/argo-cd/values.yaml

helm repo add argo-cd https://argoproj.github.io/argo-helm
helm dep update charts/argo-cd/
echo "charts/" > charts/argo-cd/.gitignore
```


## create with namespace argocd


```
kubectl create ns argocd
helm install argocd charts/argo-cd/ -n argocd
kubectl port-forward svc/argocd-server -n argocd  8080:443

```

get admin password which is the pod name
```
ckim-mbp:helmfile ckim$ kubectl get pods -l app.kubernetes.io/name=argocd-server -n argocd -o name | cut -d'/' -f 2
argocd-server-64d464ff67-k7zwq
ckim-mbp:helmfile ckim$ 
```


http://localhost:8080


### Create root app

```
mkdir -p charts/apps/templates
touch charts/apps/vlaues.yaml
vi charts/apps/Chart.yaml

helm template charts/apps | kubectl -n argocd apply -f - 

```













