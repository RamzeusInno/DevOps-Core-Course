```markdown
# Lab 6: Advanced Ansible & CI/CD - Submission

**Name:** Ramazan Gizamov
**Date:** 2026-03-04
**Lab Points:** 

---

## Task 1: Blocks & Tags (2 pts)

### Implementation

The `common` and `docker` roles have been refactored to use Ansible blocks for better task organization and error handling.

**Common Role:**
- System update block with apt cache management
- Package installation block with common packages
- Rescue blocks handle failures (apt update failures)
- Always blocks create log files and verify status

**Docker Role:**
- Repository setup block with GPG key and apt repository
- Installation block for Docker packages
- Configuration block for user groups and Python modules
- Verification block to confirm successful installation
- Rescue blocks for handling GPG key failures and retry logic

### Tag Strategy

| Tag | Description |
|-----|-------------|
| common | All tasks in common role |
| system | System update and configuration tasks |
| packages | Package installation tasks |
| docker | All tasks in docker role |
| docker_repo | Docker repository setup |
| docker_install | Docker package installation |
| docker_config | Docker user and module configuration |
| verify | Verification tasks |
| web_app | All tasks in web_app role |
| web_app_deploy | Application deployment tasks |
| web_app_wipe | Application removal tasks |
| health_check | Health check verification |
| compose | Docker Compose operations |

### Available Tags

The output of `ansible-playbook playbooks/provision.yml --list-tags` shows all available tags for selective execution.

### Selective Execution Example

Running only Docker-related tasks with `--tags "docker"` executes just the docker role tasks, skipping common role tasks.

### Research Answers

**1. What happens if rescue block also fails?**

If a rescue block fails, Ansible stops execution of the play and marks the task as failed. The always block still executes regardless of rescue block failure, but the overall play result is failure.

**2. Can you have nested blocks?**

Yes, blocks can be nested. Inner blocks can have their own rescue and always sections, while outer blocks provide additional layers of error handling. Each block's error handling is independent.

**3. How do tags inherit to tasks within blocks?**

Tags specified at the block level are automatically applied to all tasks inside that block. Additional tags can be added to individual tasks within the block, which combine with the block-level tags.

---

## Task 2: Docker Compose (3 pts)

### Implementation

The `app_deploy` role was renamed to `web_app` and completely refactored to use Docker Compose instead of direct docker_container commands.

### Role Dependencies

The `web_app` role depends on the `docker` role, ensuring Docker is installed before application deployment. This is configured in `meta/main.yml`.

### Idempotency Verification

Running the deployment playbook twice demonstrates idempotency - the first run shows changes, the second run shows all tasks as "ok" with no changes.

### Container Status

After successful deployment, the container runs with proper port mapping and health checks configured.

### Application Verification

The application responds to health checks and serves the main endpoint correctly.

---

## Task 3: Wipe Logic (1 pt)

### Implementation

Wipe logic provides safe removal of deployed applications:

- **Variable:** `web_app_wipe: false` (default in defaults/main.yml)
- **Tag:** `web_app_wipe`
- **File:** `roles/web_app/tasks/wipe.yml`
- **Safety:** Double-gating requires both variable AND tag for execution

### Test Scenarios

**Scenario 1: Normal Deployment**
Wipe tasks are skipped, application deploys normally.

**Scenario 2: Wipe Only**
Running with variable true and wipe tag removes the application without redeploying.

**Scenario 3: Clean Reinstall**
Running with variable true executes wipe first, then deploys fresh application.

**Scenario 4: Safety Check**
Running with wipe tag but without variable does not execute wipe - application continues running.

### Research Answers

**1. Why use both variable AND tag?**

This provides double protection against accidental deletion. The variable requires explicit enabling, the tag requires explicit selection. Both conditions must be met for wipe to execute, preventing mistakes.

**2. What's the difference between `never` tag and this approach?**

The `never` tag simply prevents tasks from running unless explicitly tagged. The variable+tag approach provides more control - the variable can be used in different scenarios (wipe only, clean reinstall) while maintaining safety.

**3. Why must wipe logic come BEFORE deployment?**

For clean reinstallation scenario, the old application must be removed before installing the new one. If wipe came after deployment, it would remove what was just installed, defeating the purpose.

---

## Task 4: CI/CD (3 pts)

### Workflow Configuration

GitHub Actions workflow triggers on pushes to the ansible directory, runs ansible-lint for syntax checking, and executes the deployment playbook.

### GitHub Secrets Configured

- `ANSIBLE_VAULT_PASSWORD` - Password for decrypting vaulted variables

### Status Badge

The repository README includes a status badge showing the current workflow status.

### Research Answers

**1. What are the security implications of storing SSH keys in GitHub Secrets?**

GitHub Secrets are encrypted and only exposed to workflows. They are not visible in logs or to users. This is safer than hardcoding credentials in files, but secrets should still be rotated periodically.

**2. How would you implement a staging → production deployment pipeline?**

Use different inventories for staging and production, with separate workflows or manual approval gates between environments. Staging would deploy automatically on push, production would require manual trigger or approval.

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Python externally-managed environment error | Switched from pip to apt packages (python3-docker) |
| Docker Compose version warning | Removed version attribute from compose file |
| Container name conflict on redeploy | Added recreate: always and remove_orphans: yes to compose module |
| Template variable errors | Simplified template and used correct YAML format |
| Vault password management | Created .vault_pass file and added to .gitignore |

---

## Summary

- **Total time spent:** 8-9 hours
- **What I learned:** Ansible blocks for error handling, tag-based selective execution, Docker Compose integration, safe wipe logic, GitHub Actions automation
- **Most difficult part:** Debugging the Docker Compose module and handling the Python environment restrictions in Ubuntu 24.04
```