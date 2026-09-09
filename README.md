\# DevOps FA1 – Git-Based Infrastructure as Code and Multi-Environment Container Deployment



\## 1. Project Overview



This project demonstrates a basic DevOps workflow using Git, Docker, and Terraform.



The application consists of two separate services:



\* \*\*Frontend:\*\* Nginx web server serving a simple HTML application.

\* \*\*Backend:\*\* Python Flask API providing backend functionality.



Docker is used to containerize both services, while Terraform is used to provision the Docker infrastructure.



The same Terraform configuration is used to deploy the application into three environments:



\* QA

\* UAT

\* PROD



Environment-specific configuration is provided using Terraform variable files.



\---



\## 2. Objectives



The main objectives of this project are:



1\. Create and manage a Git repository.

2\. Use Git branches and meaningful commits.

3\. Containerize frontend and backend applications using Docker.

4\. Use Terraform as Infrastructure as Code.

5\. Deploy the application into QA, UAT, and PROD environments.

6\. Validate Terraform configuration before deployment.

7\. Document the complete DevOps workflow.



\---



\## 3. Technologies Used



| Technology      | Purpose                                     |

| --------------- | ------------------------------------------- |

| Git             | Version control                             |

| GitHub          | Remote Git repository                       |

| Docker          | Application containerization                |

| Nginx           | Frontend web server                         |

| Python          | Backend programming language                |

| Flask           | Backend API framework                       |

| Terraform       | Infrastructure as Code                      |

| Docker Provider | Allows Terraform to manage Docker resources |



\---



\## 4. Project Architecture



The application uses two Docker containers.



```text

&#x20;                   User Browser

&#x20;                        |

&#x20;                        |

&#x20;                 localhost:8081

&#x20;                 localhost:8082

&#x20;                 localhost:8083

&#x20;                        |

&#x20;                        v

&#x20;             +----------------------+

&#x20;             | Frontend Container   |

&#x20;             | Nginx                |

&#x20;             | Port 80              |

&#x20;             +----------+-----------+

&#x20;                        |

&#x20;                        | /api/

&#x20;                        |

&#x20;                        v

&#x20;             +----------------------+

&#x20;             | Backend Container    |

&#x20;             | Python Flask         |

&#x20;             | Port 5000            |

&#x20;             +----------------------+

```



The frontend and backend containers communicate through a Docker network.



\---



\# 5. Project Structure



```text

devops-fa1/

│

├── docker/

│   │

│   ├── frontend/

│   │   ├── Dockerfile

│   │   ├── index.html

│   │   └── nginx.conf

│   │

│   └── backend/

│       ├── Dockerfile

│       ├── app.py

│       └── requirements.txt

│

├── terraform/

│   ├── main.tf

│   ├── variables.tf

│   ├── outputs.tf

│   │

│   └── environments/

│       ├── qa.tfvars

│       ├── uat.tfvars

│       └── prod.tfvars

│

├── .gitignore

└── README.md

```



\---



\# 6. Git Repository Initialization



The project was initialized as a Git repository from the project root.



```powershell

git init

git branch -M main

```



The project files were then added and committed.



```powershell

git add .

git commit -m "chore: initialize DevOps FA project"

```



The `main` branch is used as the primary branch.



\---



\# 7. Git Branching Strategy



Feature branches were used to organize development.



The following branches are used:



```text

main

feature/docker

feature/terraform

feature/documentation

```



\### Docker Feature



```powershell

git checkout -b feature/docker

```



Docker-related changes were committed using:



```powershell

git add docker/

git commit -m "feat: add frontend and backend Docker containers"

```



The feature branch was merged into `main`.



```powershell

git checkout main

git merge feature/docker

```



\### Terraform Feature



```powershell

git checkout -b feature/terraform

```



Terraform-related changes were committed using:



```powershell

git add terraform/

git commit -m "feat: add Terraform Docker infrastructure"

```



The branch was then merged into `main`.



```powershell

git checkout main

git merge feature/terraform

```



\### Documentation Feature



```powershell

git checkout -b feature/documentation

```



Documentation changes were committed using:



```powershell

git add README.md .gitignore

git commit -m "docs: add project documentation"

```



The branch was then merged into `main`.



\---



\# 8. Docker Containerization



Two separate Docker containers are used.



\## 8.1 Backend Container



The backend is implemented using Python and Flask.



The backend provides the following API:



```text

GET /

GET /api/hello

```



The backend also reads the `ENVIRONMENT` environment variable.



Example response:



```json

{

&#x20; "message": "Hello from the DevOps Backend!",

&#x20; "environment": "qa"

}

```



\### Build Backend Image



```powershell

docker build -t devops-backend ./docker/backend

```



\### Run Backend Container



```powershell

docker run -d --name backend --network devops-network -e ENVIRONMENT=QA devops-backend

```



\---



\## 8.2 Frontend Container



The frontend uses Nginx to serve the HTML application.



The frontend contains a button that calls the backend API.



\### Build Frontend Image



```powershell

docker build -t devops-frontend ./docker/frontend

```



\### Run Frontend Container



```powershell

docker run -d --name frontend --network devops-network -p 8081:80 devops-frontend

```



The frontend can then be accessed at:



```text

http://localhost:8081

```



\---



\# 9. Docker Networking



A Docker network is used to allow communication between the frontend and backend containers.



```powershell

docker network create devops-network

```



The frontend communicates with the backend through the Docker network rather than using `localhost`.



The backend container is given the network alias:



```text

backend

```



This allows Nginx to forward API requests to:



```text

http://backend:5000

```



\---



\# 10. Terraform Infrastructure as Code



Terraform is used to create and manage the Docker infrastructure.



The Terraform configuration creates:



\* Docker network

\* Backend Docker image

\* Frontend Docker image

\* Backend container

\* Frontend container



Terraform configuration files:



```text

terraform/

├── main.tf

├── variables.tf

├── outputs.tf

└── environments/

&#x20;   ├── qa.tfvars

&#x20;   ├── uat.tfvars

&#x20;   └── prod.tfvars

```



\---



\# 11. Terraform Initialization



Terraform is initialized using:



```powershell

cd terraform

terraform init

```



This downloads the required Terraform Docker provider.



\---



\# 12. Terraform Validation



Before deployment, the Terraform configuration is validated.



```powershell

terraform validate

```



A successful validation produces:



```text

Success! The configuration is valid.

```



Terraform formatting can also be checked using:



```powershell

terraform fmt

```



\---



\# 13. Multi-Environment Configuration



The same Terraform code is reused for QA, UAT, and PROD.



Only the environment-specific variables change.



\## QA



File:



```text

terraform/environments/qa.tfvars

```



Configuration:



```hcl

environment   = "qa"

frontend\_port = 8081

```



Deployment:



```powershell

terraform apply -var-file="environments/qa.tfvars"

```



Application URL:



```text

http://localhost:8081

```



\---



\## UAT



File:



```text

terraform/environments/uat.tfvars

```



Configuration:



```hcl

environment   = "uat"

frontend\_port = 8082

```



Deployment:



```powershell

terraform apply -var-file="environments/uat.tfvars"

```



Application URL:



```text

http://localhost:8082

```



\---



\## PROD



File:



```text

terraform/environments/prod.tfvars

```



Configuration:



```hcl

environment   = "prod"

frontend\_port = 8083

```



Deployment:



```powershell

terraform apply -var-file="environments/prod.tfvars"

```



Application URL:



```text

http://localhost:8083

```



\---



\# 14. Environment Isolation



Each environment receives its own:



\* Docker network

\* Backend container

\* Frontend container

\* Host port



For example:



```text

QA

├── qa\_network

├── qa\_backend

└── qa\_frontend

&#x20;   └── localhost:8081



UAT

├── uat\_network

├── uat\_backend

└── uat\_frontend

&#x20;   └── localhost:8082



PROD

├── prod\_network

├── prod\_backend

└── prod\_frontend

&#x20;   └── localhost:8083

```



This prevents the environments from using the same container names and host ports.



\---



\# 15. Terraform Plan



Before applying changes, Terraform can generate an execution plan.



For QA:



```powershell

terraform plan -var-file="environments/qa.tfvars"

```



For UAT:



```powershell

terraform plan -var-file="environments/uat.tfvars"

```



For PROD:



```powershell

terraform plan -var-file="environments/prod.tfvars"

```



The plan shows which Docker resources Terraform will create, modify, or destroy.



\---



\# 16. Terraform Deployment



The infrastructure is deployed using:



```powershell

terraform apply -var-file="environments/qa.tfvars"

```



or:



```powershell

terraform apply -var-file="environments/uat.tfvars"

```



or:



```powershell

terraform apply -var-file="environments/prod.tfvars"

```



After a successful deployment, Terraform displays outputs such as:



```text

Apply complete! Resources: 5 added, 0 changed, 0 destroyed.



Outputs:



backend\_container = "uat\_backend"

environment = "uat"

frontend\_container = "uat\_frontend"

frontend\_url = "http://localhost:8082"

```



\---



\# 17. Docker Deployment Verification



Running containers can be checked using:



```powershell

docker ps

```



All containers, including stopped containers, can be checked using:



```powershell

docker ps -a

```



Docker images can be checked using:



```powershell

docker images

```



Docker networks can be checked using:



```powershell

docker network ls

```



Container logs can be viewed using:



```powershell

docker logs uat\_backend

```



or:



```powershell

docker logs uat\_frontend

```



\---



\# 18. Application Testing



The frontend is accessed through the environment-specific port.



\### QA



```text

http://localhost:8081

```



\### UAT



```text

http://localhost:8082

```



\### PROD



```text

http://localhost:8083

```



The frontend page contains a \*\*Test Backend API\*\* button.



When clicked, the frontend sends a request to the Flask backend.



A successful response displays:



```text

Hello from the DevOps Backend!



Environment: uat

```



This confirms that:



1\. The frontend container is running.

2\. The backend container is running.

3\. The frontend can communicate with the backend.

4\. The correct environment variable is being used.



\---



\# 19. Useful Terraform Commands



Initialize Terraform:



```powershell

terraform init

```



Format Terraform files:



```powershell

terraform fmt

```



Validate configuration:



```powershell

terraform validate

```



View planned changes:



```powershell

terraform plan -var-file="environments/qa.tfvars"

```



Apply QA:



```powershell

terraform apply -var-file="environments/qa.tfvars"

```



Apply UAT:



```powershell

terraform apply -var-file="environments/uat.tfvars"

```



Apply PROD:



```powershell

terraform apply -var-file="environments/prod.tfvars"

```



View outputs:



```powershell

terraform output

```



Destroy the current Terraform environment:



```powershell

terraform destroy -var-file="environments/uat.tfvars"

```



\---



\# 20. Git Verification



The Git history can be viewed using:



```powershell

git log --oneline --graph --all --decorate

```



Branches can be viewed using:



```powershell

git branch

```



Repository status can be checked using:



```powershell

git status

```



The remote repository can be pushed using:



```powershell

git push -u origin main

```



Feature branches can be pushed using:



```powershell

git push -u origin feature/docker

git push -u origin feature/terraform

git push -u origin feature/documentation

```



\---



\# 21. .gitignore



The project uses `.gitignore` to prevent unnecessary or generated files from being committed.



Examples include:



```text

.terraform/

\*.tfstate

\*.tfstate.\*

.env

\_\_pycache\_\_/

\*.pyc

.vscode/

.idea/

```



The Terraform dependency lock file is retained in Git to help maintain reproducible provider versions.



\---



\# 22. Rubric Coverage



| FA Requirement                                    | Implementation                                                    |

| ------------------------------------------------- | ----------------------------------------------------------------- |

| Git Repository \& Project Initialization – 2 marks | Git repository, main branch, project structure and initial commit |

| Git Branching, Commits \& Push – 3 marks           | Feature branches, meaningful commits, merges and GitHub push      |

| Docker Containerization – 4 marks                 | Separate Nginx frontend and Flask backend containers              |

| Terraform Infrastructure as Code – 4 marks        | Terraform creates Docker network, images and containers           |

| Multi-Environment Configuration – 4 marks         | QA, UAT and PROD `.tfvars` files                                  |

| Terraform Validation \& Deployment – 2 marks       | `terraform fmt`, `validate`, `plan` and `apply`                   |

| Documentation / README – 1 mark                   | Complete project documentation and instructions                   |



\*\*Total: 20 marks\*\*



\---



\# 23. Conclusion



This project demonstrates a basic end-to-end DevOps workflow.



Git is used for version control and feature-based development. Docker is used to containerize the frontend and backend services. Terraform provides Infrastructure as Code for creating and managing the Docker infrastructure.



The same Terraform configuration is reused across QA, UAT, and PROD by changing environment-specific variables. This demonstrates a simple and repeatable multi-environment deployment approach.



The project also demonstrates Terraform validation, planning, deployment, Docker networking, application testing, Git branching, and documentation.



