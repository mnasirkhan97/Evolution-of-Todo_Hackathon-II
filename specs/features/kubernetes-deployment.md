# Feature: Local Kubernetes Deployment (Phase IV)

## Goal
Deploy the Todo Chatbot application on a local Kubernetes cluster (Minikube) using Docker containers and Helm Charts.

## Tools & Technologies
- **Containerization**: Docker (Docker Desktop)
- **Orchestration**: Kubernetes (Minikube)
- **Package Management**: Helm Charts
- **AI Ops**: Docker AI (Gordon), kubectl-ai, Kagent (simulated or utilized if available)

## Requirements

### 1. Containerization
- **Backend**: Dockerfile for FastAPI app.
- **Frontend**: Dockerfile for Next.js app.
- **Optimization**: Multi-stage builds for small image size.

### 2. Kubernetes Configuration (Helm)
- **Chart Structure**:
    - `templates/deployment.yaml`: For frontend and backend.
    - `templates/service.yaml`: ClusterIP/NodePort/LoadBalancer definitions.
    - `templates/ingress.yaml`: (Optional) Ingress config.
    - `values.yaml`: Configurable parameters (image tags, replicas, ports).
- **Database**:
    - Use ephemeral Postgres pod within command or connect to external Neon DB?
    - *Decision*: For "Cloud Native" local dev, we will typically run a Postgres pod in the cluster or stick to the Neon DB connection string injected as a secret. Given the "Stateless" nature of previous phase, let's keep using Neon DB via Secrets for simplicity and state persistence.

### 3. Deployment
- **Environment**: Minikube.
- **Commands**:
    - `docker build ...`
    - `minikube start`
    - `helm install ...`

## Verification
- **Health Check**: Pods are Running (`kubectl get pods`).
- **Access**: Application is accessible via `minikube service` or port-forwarding.
- **Functionality**: Chatbot and Task CRUD work in the K8s environment.
