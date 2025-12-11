Project: Microservices + Terraform + Docker + AWS RDS Deployment

Overview
This project demonstrates a full DevOps workflow combining:
- Local microservices containerized with Docker
- Infrastructure as Code using Terraform
- Two Terraform providers: Docker (local) and AWS (cloud)
- A complete environment suitable for a startup-style internal platform

The project includes:
- auth-service: simple login microservice (Python Flask)
- catalog-service: product listing microservice (Python Flask)
- Terraform configuration to deploy:
  - Docker images & containers (auth + catalog)
  - A PostgreSQL database hosted on AWS RDS
  - AWS networking resources (default VPC + Security Group)

Project Structure
services/
├── auth-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── catalog-service/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt

terraform/
├── main.tf
├── outputs.tf
├── terraform.tfvars
├── terraform.tfstate
└── terraform.tfstate.backup

1. Running Local Microservices (Docker Compose)
Start both services locally:
docker compose up --build

Services exposed:
- Auth service → http://localhost:5000/login
- Catalog service → http://localhost:5001/products

2. Terraform Infrastructure
Provider 1: Docker
- Builds Docker images
- Creates Docker containers
- Manages ecommerce-net network

Provider 2: AWS
- Adopts default AWS VPC
- Creates a Security Group for PostgreSQL
- Creates a managed RDS PostgreSQL instance

3. Before Running Terraform
Install AWS CLI and configure:
aws configure

Create terraform.tfvars:
aws_region  = "eu-west-3"
db_username = "startup_admin"
db_password = "StrongPassword123!"

4. Running Terraform
terraform init
terraform plan
terraform apply

Outputs include:
- Microservice URLs
- RDS endpoint
- DB name & username

5. Destroying Resources
terraform destroy
This removes:
- RDS instance
- Security group
- Docker containers & network

6. Safety Notes
- Destroy RDS after use to avoid charges
- Do not commit secrets
- terraform.tfvars is ignored by git
- Opening port 5432 globally is acceptable only for TP work

7. Useful Commands
Docker:
docker ps
docker images
docker network ls
docker compose down

Terraform:
terraform fmt
terraform validate
terraform plan
terraform apply
terraform destroy

8. Next Steps (Optional Enhancements)
- Connect catalog-service to AWS RDS
- Add Ansible deployment automation
- Add monitoring (Grafana, Prometheus)
- Add API gateway / reverse proxy
