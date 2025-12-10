


output "auth_url" {
  description = "URL de la page de login"
  value       = "http://localhost:5000/login"
}

output "catalog_url" {
  description = "URL du catalogue produits"
  value       = "http://localhost:5001/products"
}


output "azure_vm_public_ip" {
  description = "Adresse IP publique de la VM Azure"
  value       = azurerm_public_ip.vm.ip_address
}