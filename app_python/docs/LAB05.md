```markdown
# Lab 05 — Ansible Fundamentals

## 1. Architecture Overview

**Ansible version:** 2.16.3

**Target:** Local VM (VirtualBox)

**VM IP:** 127.0.0.1

**VM user:** ramzuka

**Role structure:**

```
ansible/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── playbooks/
│   ├── deploy.yml
│   └── provision.yml
├── roles/
│   ├── app_deploy/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   └── tasks/
│   │       └── main.yml
│   ├── common/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   └── tasks/
│   │       └── main.yml
│   └── docker/
│       ├── defaults/
│       │   └── main.yml
│       ├── handlers/
│       │   └── main.yml
│       └── tasks/
│           └── main.yml
├── group_vars/
│   └── all.yml
└── docs/
    └── LAB05.md
```

**Why roles instead of monolithic playbooks:**

Roles provide modularity and reusability. Each role has a specific responsibility and can be used across different playbooks and projects. This structure makes the code easier to maintain, test, and share. For example, the docker role can be reused in any project that needs Docker installed, without copying and pasting tasks.

---

## 2. Roles Documentation

### Common Role

**Purpose:** Basic system configuration and package installation that every server needs.

**Location:** `roles/common/`


**Tasks from tasks/main.yml:**

1. Update apt cache with cache_valid_time for efficiency
2. Install all packages from common_packages list
3. Set system timezone

**Handlers:** None

**Dependencies:** None

### Docker Role

**Purpose:** Install and configure Docker CE on Ubuntu systems.

**Location:** `roles/docker/`

---

**First Run Changes:**

Tasks reported as changed. These tasks actually modified the system:
- Updating apt cache (first time only)
- Installing packages (they were not present)
- Setting timezone (was not set)
- Adding Docker GPG key and repository
- Installing Docker packages
- Adding user to docker group
- Installing Python modules

**Second Run Results:**

All tasks reported as ok. Zero changes made to the system.

**Why Idempotent:**

The roles are idempotent because:

1. apt module with state=present only installs packages if not already installed
2. apt_key and apt_repository check if key/repo exists before adding
3. service module with state=started only starts service if not running
4. user module with append=yes only adds user to group if not already a member
5. cache_valid_time=3600 only updates apt cache if older than 1 hour

The system reached its desired state in the first run. The second run confirms that no changes are needed because the system already matches the desired configuration.

---

## 4. Ansible Vault Usage

### Credential Storage Strategy

Sensitive data is stored in an encrypted file using Ansible Vault.

**Location:** `group_vars/all.yml`

**Command to create encrypted file:**

```bash
ansible-vault create group_vars/all.yml --ask-vault-pass
```

### Encrypted File Content

The file `group_vars/all.yml` contains encrypted data:

```
$ANSIBLE_VAULT;1.1;AES256
66386439653236336...
```

The decrypted content is:

```yaml
---
# Docker Hub credentials
dockerhub_username: ramzeus1
dockerhub_password: dckr_pat_pC4gjbebQ4Z4PAFVN4VcK8XTsAs
# Application configuration
app_name: devops-app
docker_image_tag: latest
app_port: 5000
app_container_name: "{{ app_name }}"
restart_policy: unless-stopped
```

### Why Ansible Vault is Important

1. Security: Prevents exposing credentials in version control
2. Compliance: Meets security requirements for handling secrets
3. Collaboration: Encrypted files can be safely shared in repos
4. Separation: Separates code from configuration and secrets
5. Auditability: Clear what is encrypted and what is not


## 6. Key Decisions

**Why use roles instead of plain playbooks?**

Roles provide better organization and reusability. Each role encapsulates a specific functionality that can be independently developed, tested, and reused across different playbooks and projects. This modularity also makes the code easier to maintain and understand.

**How do roles improve reusability?**

Roles can be shared across multiple playbooks and even different projects. For example, the Docker role can be used in any project that needs Docker installed, without rewriting the same tasks. Roles can also be published to Ansible Galaxy for community use.

**What makes a task idempotent?**

A task is idempotent when running it multiple times produces the same result without unintended side effects. In Ansible, this is achieved by using modules that check the current state before making changes. For example, the apt module with state=present only installs a package if it is not already installed.

**How do handlers improve efficiency?**

Handlers run only when notified by tasks and execute only once at the end of the play, even if notified multiple times. This prevents unnecessary service restarts. For example, if multiple configuration files change, Docker is restarted only once, not after each change.

**Why is Ansible Vault necessary?**

Ansible Vault is necessary to securely store sensitive information like passwords, API tokens, and private keys in version control. Without it, these secrets would be exposed in plain text, creating security vulnerabilities. Vault encrypts the data while keeping it in the same repository as the code.

---

## 7. Challenges Encountered

- Repository key issue: Initially had problems with Docker GPG key. Solved by using the correct key URL and apt_key module.
- User group addition: Required logout or session refresh to take effect. Added notification to restart Docker service.
- Health check timing: Application needed time to start. Added wait_for task before health check.
- Vault password management: Created .vault_pass file and added to .gitignore to prevent accidental commit.
- Idempotency in apt update: Used cache_valid_time to avoid unnecessary updates on every run.
- Local VM networking: Had to configure port forwarding to access the application from host machine.
```