# Modulo 7 - Projeto 2 - Segurança em Azure

Este projeto teve como objetivos:
1. Fazer deploy no Azure Kubernetes Services (AKS) da aplicação desenvolvida anteriormente
2. Implementar monitorização dos pods e da aplicação, com o Prometheus
3. Integrar a análise de vulnerabilidades de segurança com o Trivy em pipelines CI/CD
4. Integrar testes de penetração da API com OWASP ZAP em pipelines CI/CD


1- Criar um serviço de LoadBalancer

2- Criar um deployment com a imagem que contém a aplicação


(
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update)


MINIKUBE:

minikube start

alias kubectl="minikube kubectl --"

kubectl create secret generic regcred     --from-file=.dockerconfigjson=<path-to>/.docker/config.json     --type=kubernetes.io/dockerconfigjson
