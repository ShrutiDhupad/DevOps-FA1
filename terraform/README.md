\# Terraform Infrastructure



Terraform provisions the Docker infrastructure for this project.



It creates:



\- Docker network

\- Backend Docker image and container

\- Frontend Docker image and container



The same Terraform configuration is used for QA, UAT, and PROD.

Environment-specific settings are stored in the environments folder.

