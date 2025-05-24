# Modulo 7 - Projeto 2 - Segurança em Azure

Este projeto teve como objetivos:
1. Fazer deploy no Azure Kubernetes Services (AKS) da aplicação desenvolvida anteriormente
2. Implementar monitorização dos pods e da aplicação, com o Prometheus
3. Integrar a análise de vulnerabilidades de segurança com o Trivy em pipelines CI/CD
4. Integrar testes de penetração da API com OWASP ZAP em pipelines CI/CD


## 1. Deploy no AKS

1.1 - Criar namespace dentro do cluster (grupo3)
```
az aks get-credentials --resource-group <RG_name> \
--name <cluster_name>
```
```
kubectl create namespace grupo3
```

1.2- Criar um [PersistentVolumeClaim]
```
kubectl apply -f api-pvc.yaml -n grupo3
```

1.3- Criar secret para poder aceder ao ACR (Azure Container Registry)
```
kubectl create secret generic regcred \
--from-file=.dockerconfigjson=<path-to>/.docker/config.json \
--type=kubernetes.io/dockerconfigjson \
-n grupo3

```
1.4- Fazer um [Deployment] da aplicação web
```
kubectl apply -f api-webapp.yaml -n grupo3
```

1.5- Criar um serviço de [LoadBalancer]
```
kubectl apply -f api-loadbalancer.yaml -n grupo3
```

## 2. Monitorização com Prometheus e Grafana

2.1- Adicionar o repositório "prometheus-community" ao Helm

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

2.2- Instalar pacote com Prometheus e Grafana
```
helm install <RELEASE_NAME> prometheus-community/kube-prometheus-stack \
-n grupo3 -f config-values.yaml
```

2.3- Instalar biblioteca python (django-prometheus) de cliente Prometheus na aplicação web.

2.4- Criar um [ServiceMonitor], para definir onde procurar as métricas e as configurações de monitorização da webapp
```
kubectl apply -f api-servicemonitor.yaml -n grupo3
```
2.5- Configurar [dashboard] no Grafana 

## 3. Integrar o Trivy (Análise Estática) e OWASP ZAP (PenTest) numa pipeline CI/CD

- [Pipeline CI] (Trivy: Dockerfile)

- [Pipeline CD] (Trivy: Imagem Docker + OWASP ZAP (API))

## Contributors:
- André Rocha
- Pedro Pires
- Waltenberg Dantas

[PersistentVolumeClaim]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-pvc.yaml?ref_type=heads
[Deployment]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-webapp.yaml?ref_type=heads
[LoadBalancer]:https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-loadbalancer.yaml?ref_type=heads
[ServiceMonitor]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/kubernetes/api-servicemonitor.yaml?ref_type=heads
[dashboard]: http://9.163.14.42/d/85a562078cdf77779eaa1add43ccec1t/kubernetes-api-django-http?orgId=1&from=now-1h&to=now&timezone=utc&var-datasource=default&var-cluster=&var-namespace=grupo3&refresh=10s
[Pipeline CI]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/.github/workflows/pipeline_CI.yml?ref_type=heads
[Pipeline CD]: https://gitlab.com/lezz-git-it/webapp/-/blob/main/.github/workflows/pipeline_CD.yml?ref_type=heads