# Modulo 7 - Projeto 2 - Segurança em Azure

Este projeto teve como objetivos:
1. Fazer deploy no Azure Kubernetes Services (AKS) da aplicação desenvolvida anteriormente
2. Implementar monitorização dos pods e da aplicação, com o Prometheus
3. Integrar a análise de vulnerabilidades de segurança com o Trivy em pipelines CI/CD
4. Integrar testes de penetração da API com OWASP ZAP em pipelines CI/CD


## Deploy no AKS

1- Criar namespace dentro do cluster (grupo3)
```
az aks get-credentials --resource-group <RG_name> --name <cluster_name>

kubectl create namespace grupo3
```

2- Criar um [PersistentVolumeClaim]
```
kubectl apply -f api-pvc.yaml -n grupo3
```

3- Fazer um [Deployment] da aplicação web
```
kubectl apply -f api-webapp.yaml -n grupo3
```

4- Criar um serviço de [LoadBalancer]
```
kubectl apply -f api-loadbalancer.yaml -n grupo3
```

## Monitorização com Prometheus e Grafana

1- Adicionar o repositório "prometheus-community" ao Helm

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

2- Instalar pacote com Prometheus e Grafana
```
helm install <RELEASE_NAME> prometheus-community/kube-prometheus-stack -n grupo3 -f config-values.yaml
```

3- Instalar biblioteca python de cliente Prometheus na aplicação web.

4- Criar um [ServiceMonitor], para definir onde procurar as métricas e as configurações de monitorização da webapp
```
kubectl apply -f api-servicemonitor.yaml -n grupo3
```
5- Configurar [dashboard] no Grafana 

##



MINIKUBE:

minikube start

alias kubectl="minikube kubectl --"

kubectl create secret generic regcred     --from-file=.dockerconfigjson=<path-to>/.docker/config.json     --type=kubernetes.io/dockerconfigjson

[PersistentVolumeClaim]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-pvc.yaml?ref_type=heads
[Deployment]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-webapp.yaml?ref_type=heads
[LoadBalancer]:https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-loadbalancer.yaml?ref_type=heads
[ServiceMonitor]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-servicemonitor.yaml?ref_type=heads
[dashboard]: http://9.163.14.42/d/85a562078cdf77779eaa1add43ccec1t/kubernetes-api-django-http?orgId=1&from=now-1h&to=now&timezone=utc&var-datasource=default&var-cluster=&var-namespace=grupo3&refresh=10s