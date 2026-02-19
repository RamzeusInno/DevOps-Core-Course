# Lab 4 — Infrastructure as Code

## Cloud Provider & Infrastructure
- **Provider:** Local VM (VirtualBox)
- **Reason:** Free, full control, no cloud costs
- **VM Specs:** Ubuntu 24.04 LTS, 2GB RAM, 20GB disk, NAT + port forwarding (2222→22)
- **SSH Access:** `ssh devops@localhost -p 2222`

## Terraform Implementation
- **Version:** 1.9.8
- **Code:** Creates local files describing the VM
- **Files created:**
  - `vm_terraform_info.txt` — VM information
  - `ansible_inventory.ini` — Ansible inventory
- **Screenshot:** ![Terraform apply](screenshots/terraform-apply.png)

## Pulumi Implementation
- **Version:** latest
- **Language:** Python
- **Code:** Same functionality with Python
- **Files created:**
  - `vm_pulumi_info.txt` — VM information
  - `pulumi_ansible_inventory.ini` — Ansible inventory
- **Screenshot:** ![Pulumi up](screenshots/pulumi-up.png)

## Terraform vs Pulumi
| Aspect | Terraform | Pulumi |
|--------|-----------|--------|
| Language | HCL (declarative) | Python (imperative) |
| Learning | Easy syntax | Requires Python |
| Readability | Very clear | Flexible but more code |
| Debugging | Limited | Full Python debug |
| Best for | Pure infrastructure | Infra + app logic |

## Lab 5 Preparation
- Keeping VM running
- SSH: `ssh devops@localhost -p 2222`
- Ansible inventory: `ansible_inventory.ini`
- Docker ready to install when needed