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
```
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
├── terraform.tfvars     # ignored by git
├── terraform.tfstate    # generated
└── terraform.tfstate.backup
```


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

Create terraform.tfvars (example):
aws_region  = "eu-west-3"
db_username = "startup_admin"
db_password = "StrongPassword123!"

4. Running Terraform
From inside /terraform:
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
- Opening port 5432 globally is acceptable only for TP work (restrict in production)

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

8. Next Steps (Project Roadmap)
Step 1 — Apply the infrastructure (Docker + AWS)
- Run: terraform apply
- Verify Docker containers are running:
  - http://localhost:5000/login
  - http://localhost:5001/products
- Capture Terraform outputs (especially rds_endpoint)

Step 2 — Initialize the PostgreSQL schema on AWS RDS
- Connect to RDS using psql / pgAdmin / DBeaver
- Create a minimal schema:
  - table products(id, name, description, price)
- Insert a few sample rows (seed data)

Step 3 — Connect catalog-service to AWS RDS
- Add a PostgreSQL client dependency in catalog-service (psycopg2-binary or SQLAlchemy)
- Add an environment variable to the catalog container (e.g., DATABASE_URL)
- Update /products to query the products table instead of returning static data

Step 4 — Improve security (recommended)
- Restrict the Security Group ingress (5432) to your public IP instead of 0.0.0.0/0
- Optional: set publicly_accessible = false and use a bastion/EC2 (advanced)

Step 5 — Optional functional features (nice for the report)
- Add a leads table + route (e.g., POST /lead) to store emails
- Protect admin routes using auth-service tokens

Step 6 — Optional DevOps enhancements
- Add CI checks (terraform fmt/validate, lint, docker build)
- Add monitoring (Prometheus/Grafana) and basic healthchecks
- Add an API gateway / reverse proxy (Nginx/Traefik)

Author
Victor Verdier
DevOps / Cloud / Microservices Project
