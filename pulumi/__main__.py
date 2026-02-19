import pulumi
from datetime import datetime

vm_info_content = f"""
This file represents the infrastructure created by Pulumi for Lab 4.
VM Name: devops-vm
SSH User: devops
SSH Port (Host): 2222
OS: Ubuntu 24.04 LTS
Managed by: Pulumi (Python)
Created at: {datetime.now().isoformat()}
"""

with open('./vm_pulumi_info.txt', 'w') as f:
    f.write(vm_info_content)

inventory_lines = [
    "[devops_vm]",
    "devops-vm ansible_host=localhost ansible_port=2222 ansible_user=devops"
]
inventory_content = "\n".join(inventory_lines)
with open('../pulumi_ansible_inventory.ini', 'w') as f:
    f.write(inventory_content)

pulumi.export('vm_info_file', './vm_pulumi_info.txt')
pulumi.export('ansible_inventory', '../pulumi_ansible_inventory.ini')
pulumi.export('timestamp', datetime.now().isoformat())
