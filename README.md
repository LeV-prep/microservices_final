Project: Microservices + Terraform + Docker + AWS RDS + Ansible

Overview
This project demonstrates a complete infrastructure automation workflow combining:
- Dockerized microservices
- Infrastructure provisioning with Terraform
- Configuration management with Ansible
- Cloud resources on AWS (RDS PostgreSQL)
- A reproducible Terraform → Ansible pipeline

The goal of the project is not application complexity, but infrastructure automation,
reproducibility, and clarity, as required by the TP3 specifications.

------------------------------------------------------------

Architecture Overview

Microservices:
- auth-service: authentication microservice (Python Flask)
- catalog-service: product catalog microservice (Python Flask)

Infrastructure components:
- Docker images and containers (managed by Terraform)
- Docker network (ecommerce-net)
- AWS RDS PostgreSQL database
- AWS Security Group (PostgreSQL access)
- Ansible roles for service configuration
- Python script orchestrating the full pipeline

------------------------------------------------------------

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
├── terraform.tfvars     # ignored by git
├── terraform.tfstate    # generated
└── terraform.tfstate.backup

ansible/
├── inventory/
│   └── inventory.ini    # generated dynamically
├── roles/
│   ├── common/
│   ├── auth/
│   └── catalog/
└── playbook.yml

deploy.py                # Python entrypoint for the pipeline

------------------------------------------------------------

Prerequisites

1) Docker
docker --version
docker info

2) Terraform
terraform --version

3) AWS CLI (required for Terraform AWS provider)
aws --version
aws configure
aws sts get-caller-identity

Terraform automatically uses AWS credentials configured via the AWS CLI.

4) Ansible
ansible --version

------------------------------------------------------------

Terraform Variables

Create the file terraform/terraform.tfvars:

aws_region  = "eu-west-3"
db_username = "startup_admin"
db_password = "StrongPassword123!"

Important:
- This file is ignored by Git
- Never commit secrets

------------------------------------------------------------

Main Deployment Workflow (Terraform)

From the terraform/ directory:

terraform init
terraform fmt
terraform validate
terraform plan
terraform apply

Terraform provisions:
- Docker images
- Docker containers
- Docker network
- AWS RDS PostgreSQL instance
- AWS Security Group

------------------------------------------------------------

Terraform Outputs

Terraform outputs expose:
- Microservice URLs (localhost)
- RDS endpoint
- Database name
- Database username
- Ports and connection information required by Ansible

These outputs are consumed by Ansible and the Python orchestration script.

------------------------------------------------------------

Configuration Management (Ansible)

Ansible is used after Terraform to configure services and application behavior.

Responsibilities:
- Configure application environment variables
- Configure database connection
- Ensure idempotent service setup
- Apply templates and handlers

Ansible inventory is generated dynamically using Terraform outputs
(no fully static inventory).

Run Ansible manually (debug):
ansible-playbook -i ansible/inventory/inventory.ini ansible/playbook.yml

------------------------------------------------------------

Python Orchestration Script

A Python script (deploy.py) acts as the single entry point of the pipeline.

Responsibilities:
- Launch Terraform (init / apply)
- Parse Terraform outputs
- Generate Ansible inventory
- Execute Ansible playbooks
- Optionally trigger basic validation tests

Example:
python deploy.py deploy
python deploy.py destroy

------------------------------------------------------------

Optional: Docker Compose (Local Debug Only)

Docker Compose is optional and NOT part of the main deployment pipeline.

It can be used only for local debugging without Terraform:

docker compose up --build

Warning:
Do not use Docker Compose and Terraform Docker provider at the same time.

------------------------------------------------------------

Destroying Resources

terraform destroy

This removes:
- AWS RDS instance
- Security Group
- Docker containers
- Docker network

Always destroy AWS resources after TP work to avoid cloud charges.

------------------------------------------------------------

Safety Notes

- Do not commit secrets
- terraform.tfvars is ignored by git
- PostgreSQL port (5432) is open publicly for TP purposes only
- In production, restrict access to trusted IPs

------------------------------------------------------------

Roadmap (TP3 Alignment)

Step 1 — Infrastructure provisioning (Terraform)
- Provision Docker containers and AWS RDS
- Expose all required outputs

Step 2 — Configuration management (Ansible)
- Create at least two Ansible roles (common + service roles)
- Use templates (Jinja2) for configuration
- Ensure idempotence and handlers
- Consume Terraform outputs dynamically

Step 3 — Pipeline orchestration (Python)
- Implement a single Python entrypoint (deploy.py)
- Chain Terraform → Ansible automatically
- Allow full redeploy after destruction

Step 4 — Validation and demonstration
- Verify exposed services
- Demonstrate reproducibility
- Present architecture, pipeline, and automation choices

------------------------------------------------------------

Author
Victor Verdier
DevOps / Cloud / Infrastructure Automation Project
