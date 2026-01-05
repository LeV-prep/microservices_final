############################################################
# 1. Configuration Terraform + Provider Docker
############################################################

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


# Provider Docker : Terraform va parler au daemon Docker local
provider "docker" {}

provider "aws" {
  region = var.aws_region
  # Les credentials sont pris par :
  # - aws configure
  # - ou variables d'env: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
}


############################################################
# 2. Réseau Docker pour nos microservices
############################################################

resource "docker_network" "ecommerce" {
  name = "ecommerce-net"
}


############################################################
# 3. Images Docker : build à partir des Dockerfile
############################################################

# Image pour auth-service
resource "docker_image" "auth" {
  name = "auth-service:latest"

  build {
    # chemin par rapport au dossier terraform/
    context    = "${path.module}/../services/auth-service"
    dockerfile = "Dockerfile"
  }
}

# Image pour catalog-service
resource "docker_image" "catalog" {
  name = "catalog-service:latest"

  build {
    context    = "${path.module}/../services/catalog-service"
    dockerfile = "Dockerfile"
  }
}


############################################################
# 4. Conteneur auth-service
############################################################

#Finalement c'est ansible qui va le créer



############################################################
# 5. Conteneur catalog-service
############################################################

#Finalement c'est ansible qui va le créer




############################################################
# Variables
############################################################

# Région AWS
variable "aws_region" {
  type        = string
  description = "Région AWS où créer les ressources"
}

# Identifiants de la base PostgreSQL RDS
variable "db_username" {
  type        = string
  description = "Nom d'utilisateur admin pour la base PostgreSQL"
}

variable "db_password" {
  type        = string
  description = "Mot de passe admin pour la base PostgreSQL"
  sensitive   = true
}



############################################################
# 6. AWS : Base de données RDS PostgreSQL
############################################################

# On récupère le VPC par défaut de la région choisie
resource "aws_default_vpc" "default" {}

# Security Group pour autoriser l'accès à PostgreSQL
resource "aws_security_group" "db" {
  name        = "startup-db"
  description = "Security group pour la base PostgreSQL de la startup"
  vpc_id      = aws_default_vpc.default.id

  # Ingress : autoriser TCP 5432 depuis partout (pour un TP).
  # En vrai : à restreindre à ton IP uniquement.
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress : autoriser tout vers l'extérieur
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Instance RDS PostgreSQL
resource "aws_db_instance" "startup_catalog" {
  identifier = "startup-catalog-db"

  engine = "postgres"
  #engine_version = "15.7"        # tu peux adapter si besoin
  instance_class = "db.t3.micro" # free tier friendly

  allocated_storage = 20

  db_name  = "startup_catalog"
  username = var.db_username
  password = var.db_password

  # Associer le SG qu'on vient de créer
  vpc_security_group_ids = [aws_security_group.db.id]

  publicly_accessible = true
  skip_final_snapshot = true

  # Optionnel : pour éviter des petites surprises
  deletion_protection = false
}


############################################################
# Outputs AWS
############################################################

output "rds_endpoint" {
  value       = aws_db_instance.startup_catalog.address
  description = "Endpoint de la base PostgreSQL RDS"
}

output "rds_db_name" {
  value       = aws_db_instance.startup_catalog.db_name
  description = "Nom de la base de données"
}

output "rds_username" {
  value       = var.db_username
  description = "Utilisateur admin de la base"
}
