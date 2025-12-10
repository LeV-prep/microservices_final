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

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}


# Provider Docker : Terraform va parler au daemon Docker local
provider "docker" {}

provider "azurerm" {
  features {}
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

resource "docker_container" "auth" {
  name  = "auth-service"
  image = docker_image.auth.image_id   # image buildée juste au-dessus

  must_run = true
  restart  = "no"

  # Exposer le port 5000 du conteneur vers 5000 sur ta machine
  ports {
    internal = 5000
    external = 5000
    ip       = "0.0.0.0"
    protocol = "tcp"
  }

  env = [
    "SERVICE_NAME=auth",
    "ENVIRONMENT=dev",
  ]

  networks_advanced {
    name = docker_network.ecommerce.name
  }
}


############################################################
# 5. Conteneur catalog-service
############################################################

resource "docker_container" "catalog" {
  name  = "catalog-service"
  image = docker_image.catalog.image_id

  must_run = true
  restart  = "no"

  # Exposer le port 5001 du conteneur vers 5001 sur ta machine
  ports {
    internal = 5001
    external = 5001
    ip       = "0.0.0.0"
    protocol = "tcp"
  }

  env = [
    "SERVICE_NAME=catalog",
    "ENVIRONMENT=dev",
  ]

  networks_advanced {
    name = docker_network.ecommerce.name
  }

  # Optionnel : s'assurer que le réseau existe avant
  depends_on = [
    docker_network.ecommerce,
    docker_container.auth
  ]
}





############################################################
# 6. Azure : Resource Group, réseau, VM Linux
############################################################

# Région Azure (West Europe = data center en Europe)
variable "azure_location" {
  type    = string
  default = "francecentral"
}

# Nom d'utilisateur pour la VM
variable "azure_admin_username" {
  type    = string
  default = "victor"
}

# Ta clé SSH publique (contenu de ton id_rsa.pub)
variable "azure_admin_ssh_public_key" {
  description = "Clé SSH publique pour se connecter à la VM Azure"
  type        = string
}

# 6.1 Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-microservices-final"
  location = var.azure_location
}

# 6.2 Réseau virtuel
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-microservices"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# 6.3 Subnet
resource "azurerm_subnet" "subnet" {
  name                 = "subnet-main"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# 6.4 IP publique
resource "azurerm_public_ip" "vm" {
  name                = "pip-vm-microservices"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  allocation_method   = "Static"
  sku                 = "Standard"
  sku_tier            = "Regional"
}


# 6.5 Network Security Group (ouvrir SSH + HTTP)
resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-microservices"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "HTTP"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# 6.6 Interface réseau
resource "azurerm_network_interface" "nic" {
  name                = "nic-vm-microservices"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.vm.id
  }
}

# 6.7 Associer le NSG à la NIC
resource "azurerm_network_interface_security_group_association" "nic_nsg" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# 6.8 VM Linux (Ubuntu) taille petite (éligible free tier)
resource "azurerm_linux_virtual_machine" "vm" {
  name                = "vm-microservices"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  size                = "Standard_B1s"

  admin_username      = var.azure_admin_username

  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]

  admin_ssh_key {
    username   = var.azure_admin_username
    public_key = var.azure_admin_ssh_public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}
