# 部署

- Docker：`docker build -t sciforge . && docker run -p 8000:8000 sciforge`
- K8s：`kubectl apply -f deploy/k8s/`
- Helm：`helm install sciforge deploy/helm/sciforge`
