# DevOps FA1 — Git-Based Infrastructure as Code and Multi-Environment Container Deployment

## 1. Project Overview

This project demonstrates Git-based Infrastructure as Code using Terraform and Docker.

The application contains two containers:

* Frontend — Nginx
* Backend — Python Flask API

Terraform is used to provision the Docker network, Docker images and Docker containers.

The same Terraform configuration supports three environments:

* QA
* UAT
* PROD

Environment-specific settings are stored in `.tfvars` files.

---

## 2. Architecture

```text
                    Browser
                       |
                       v
              +----------------+
              |    Frontend    |
              |  Nginx Docker  |
              +----------------+
                       |
                       | HTTP
                       v
              +----------------+
              |    Backend     |
              |  Flask Docker  |
              +----------------+
```

Both containers are connected to an environment-specific Docker network.

---

## 3. Technologies

* Git
* GitHub
* Docker
* Dockerfile
* Terraform
* Python
* Flask
* Nginx

---

## 4. Project Structure

```text
devops-fa1/
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── environments/
│       ├── qa.tfvars
│       ├── uat.tfvars
│       └── prod.tfvars
│
├── docker/
│   ├── frontend/
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   └── index.html
│   │
│   └── backend/
│       ├── Dockerfile
│       ├── app.py
│       └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## 5. Backend

The backend is a Python Flask API.

The API provides:

```text
GET /
GET /api/hello
```

The environment is passed to the backend using the `ENVIRONMENT` environment variable.

---

## 6. Frontend

The frontend is served using Nginx.

Nginx also acts as a reverse proxy and forwards `/api/` requests to the backend container.

---

## 7. Docker

Build the backend:

```bash
docker build -t devops-backend ./docker/backend
```

Build the frontend:

```bash
docker build -t devops-frontend ./docker/frontend
```

Docker containers are connected using a user-defined Docker network.

---

## 8. Terraform Initialization

Navigate to the Terraform directory:

```bash
cd terraform
```

Initialize Terraform:

```bash
terraform init
```

Format Terraform:

```bash
terraform fmt
```

Validate the configuration:

```bash
terraform validate
```

---

## 9. QA Deployment

Create a Terraform plan:

```bash
terraform plan -var-file="environments/qa.tfvars"
```

Deploy:

```bash
terraform apply -var-file="environments/qa.tfvars"
```

QA frontend:

```text
http://localhost:8081
```

---

## 10. UAT Deployment

Destroy the QA environment:

```bash
terraform destroy -var-file="environments/qa.tfvars"
```

Deploy UAT:

```bash
terraform apply -var-file="environments/uat.tfvars"
```

UAT frontend:

```text
http://localhost:8082
```

---

## 11. PROD Deployment

Destroy UAT:

```bash
terraform destroy -var-file="environments/uat.tfvars"
```

Deploy PROD:

```bash
terraform apply -var-file="environments/prod.tfvars"
```

PROD frontend:

```text
http://localhost:8083
```

---

## 12. Multi-Environment Design

The project uses one Terraform configuration for all environments.

The following files contain environment-specific values:

```text
qa.tfvars
uat.tfvars
prod.tfvars
```

For example:

```bash
terraform apply -var-file="environments/qa.tfvars"
```

and:

```bash
terraform apply -var-file="environments/uat.tfvars"
```

use the same `main.tf`, `variables.tf` and `outputs.tf`.

No separate Terraform infrastructure code is created for QA, UAT or PROD.

---

## 13. Git Workflow

The project uses feature branches:

```text
main
├── feature/docker
├── feature/terraform
└── feature/documentation
```

Changes are committed separately and merged into the main branch.

---

## 14. Validation

Terraform configuration was validated using:

```bash
terraform fmt
terraform validate
terraform plan
```

Docker containers were verified using:

```bash
docker ps
docker network ls
```

The frontend and backend were tested through the browser.

---

## 15. Conclusion

This project demonstrates:

* Git version control
* Git branching
* Docker containerization
* Frontend and backend containers
* Terraform Infrastructure as Code
* Environment variables
* QA/UAT/PROD configuration
* Terraform validation and deployment
* Documentation
