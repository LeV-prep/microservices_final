# Project: Microservices + Terraform + Azure Deployment

## Overview
This project demonstrates a full DevOps workflow:
- Local microservices containerized with Docker.
- Local orchestration using Docker Compose.
- Cloud infrastructure deployed on Microsoft Azure using Terraform.
- Two Terraform providers: Docker (local) and Azure (cloud).

The project includes:
- `auth-service`: simple login microservice (Python Flask)
- `catalog-service`: simple catalog/product listing (Python Flask)
- Terraform configuration to deploy:
  - local Docker containers (auth + catalog)
  - an Azure Linux virtual machine (Ubuntu)
  - required Azure networking (resource group, VNet, subnet, NSG, public IP)

---

## Project Structure

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

---

## 1. Running Local Microservices (Docker Compose)

Start the services:

docker compose up --build

Services exposed:
- Auth service → http://localhost:5000/login
- Catalog service → http://localhost:5001/products

Both services run inside the ecommerce-net Docker network.

---

## 2. Terraform Infrastructure

Terraform uses two providers:

Provider 1: Docker
Terraform builds and launches the same microservices as Docker Compose:
- Builds images from services/auth-service/Dockerfile
- Builds images from services/catalog-service/Dockerfile
- Creates Docker containers
- Creates the ecommerce-net Docker network

Provider 2: Azure (azurerm)
Terraform deploys:
- 1 Resource Group
- 1 Virtual Network + Subnet
- 1 Network Security Group (allowing SSH 22 + HTTP 80)
- 1 Public IP
- 1 Network Interface
- 1 Linux Virtual Machine (Ubuntu 22.04)

VM uses your SSH public key defined in terraform.tfvars.

---

## 3. Before Running Terraform

Install Azure CLI (Windows MSI)
Then login:

az login

Make sure your subscription is:
Azure for Students

Create the terraform.tfvars file
Example:

azure_admin_username       = "victor"
azure_admin_ssh_public_key = "ssh-ed25519 AAAA.... victor@TQTCASEGERE"

---

## 4. Running Terraform

From inside /terraform:

terraform init
terraform plan
terraform apply

Outputs will include:
- Local microservices URLs
- Azure VM public IP

To SSH into the VM:

ssh victor@<PUBLIC_IP>

---

## 5. Destroying Resources (Important)

To avoid any Azure cost:

terraform destroy

This removes:
- Azure VM
- Network resources
- Public IP
- Docker containers & images (managed by Terraform)

---

## 6. Safety Notes

- Azure for Students does NOT require a credit card.
- Using a small VM (Standard_B1s) stays within free credits.
- Destroy resources after usage.
- Keep SSH public key safe (private key never committed to Git).

---

## 7. Useful Commands

Docker
docker ps
docker images
docker network ls
docker compose down

Terraform
terraform fmt
terraform validate
terraform plan
terraform apply
terraform destroy

---

## 8. Next Steps (Optional Enhancements)

- Configure Ansible to manage the Azure VM.
- Deploy a simple web server (nginx) on the VM.
- Link microservices to a remote database.
- Add monitoring (Prometheus + Grafana).
- Add reverse proxy (Traefik / Nginx).

---

## Author
Victor Verdier
DevOps / Cloud / Microservices Project
