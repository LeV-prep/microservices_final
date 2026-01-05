# Microservices E-commerce — Terraform + Ansible + Docker + AWS RDS

## Overview

This project demonstrates a **fully automated, reproducible DevOps pipeline** for a
mini e-commerce application based on microservices.

The focus of the project is **infrastructure automation and configuration management**,
not application complexity.

The pipeline combines:

- **Terraform** for infrastructure provisioning
- **AWS RDS (PostgreSQL)** for persistent data
- **Docker** for containerized microservices
- **Ansible** for application configuration and database initialization
- **Python** as a single orchestration entrypoint

The entire stack can be **destroyed and recreated from scratch** using a single command.

---

## Architecture Overview

### Microservices

- **auth-service**
  - Handles user authentication
  - Validates credentials against PostgreSQL
  - Redirects authenticated users to the catalog

- **catalog-service**
  - Displays the product catalog
  - Reads products directly from PostgreSQL

Both services are written in **Python (Flask)** and run as Docker containers.

---

### Infrastructure Components

- **AWS RDS PostgreSQL**
  - Central database for users and products
  - Publicly accessible for TP purposes
- **AWS Security Group**
  - Allows inbound access on port `5432`
- **Docker network**
  - Allows inter-service communication
- **Local Docker daemon**
  - Runs the microservices containers

---

## Responsibilities by Tool

### Terraform — Infrastructure Provisioning

Terraform is responsible for:

- Creating the AWS RDS PostgreSQL instance
- Creating the Security Group
- Exposing infrastructure information via outputs:
  - RDS endpoint
  - Database name
  - Database username

Terraform **does not manage application containers**.
This separation avoids configuration drift and keeps Terraform focused on infrastructure.

> **Design choice:**  
> The database is intentionally destroyed during `terraform destroy`.
> This allows full reproducibility and clean testing on a new machine.
> No final snapshot is kept (`skip_final_snapshot = true`) as required for TP usage.

---

### Ansible — Configuration & Runtime Management

Ansible is responsible for:

- Reading Terraform outputs dynamically
- Initializing the database schema (tables + seed data)
- Creating and running containers with the correct environment variables
- Injecting database credentials into services

---

### Database Initialization (Ansible)

The database is initialized automatically using `init.sql`:

- Creates tables:
  - `users`
  - `products`
- Inserts initial data (seed)

---

## Deployment

### Prerequisites

- Docker Desktop (running)
- WSL with Ubuntu
- Terraform
- Ansible
- AWS credentials configured locally (`aws configure`)

### Terraform variables

Terraform variables are not stored in the repository.

Before deployment, create the following file:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Then edit terraform/terraform.tfvars and set your own values:

```bash
aws_region  = "eu-west-3"
db_username = "startup_admin"
db_password = "YourOwnStrongPassword"
```


### Database credentials

The database password is **not stored in the repository**.

Before deployment, export a database password as an environment variable:

```bash
export DB_PASSWORD="VeryStrongPassword123!"
```

This password will be used by:
- Terraform to create the PostgreSQL RDS instance
- Ansible to initialize the database and configure the services

### Deploy

```bash
python3 deploy.py deploy
```

---

## Destruction

```bash
python3 deploy.py destroy
```

---

## Author

Victor Verdier  
DevOps / Cloud / Infrastructure Automation  
TP Microservices
