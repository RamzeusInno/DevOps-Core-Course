terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "vm_info" {
  content  = <<-EOT
This file represents the infrastructure created by Terraform for Lab 4.
VM Name: ubuntu2
SSH User: ramzuka
SSH Port (Host): 2222
OS: Ubuntu 24.04 LTS
Managed by: Terraform
Created at: ${timestamp()}
EOT
  filename = "${path.module}/vm_terraform_info.txt"
}

resource "local_file" "ansible_inventory" {
  content  = <<-EOT
[devops_vm]
devops-vm ansible_host=localhost ansible_port=2222 ansible_user=devops
EOT
  filename = "${path.module}/../ansible_inventory.ini"
}

output "vm_info_file_created" {
  value = local_file.vm_info.filename
}

output "ansible_inventory_file" {
  value = local_file.ansible_inventory.filename
}