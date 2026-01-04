#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from getpass import getpass

ROOT = Path(__file__).resolve().parent
TERRAFORM_DIR = ROOT / "terraform"
ANSIBLE_DIR = ROOT / "ansible"
INVENTORY = ANSIBLE_DIR / "inventory" / "inventory.ini"
PLAYBOOK = ANSIBLE_DIR / "playbook.yml"

def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)

def get_db_password() -> str:
    # Prefer env var to avoid typing each time
    pwd = os.getenv("DB_PASSWORD")
    if pwd:
        return pwd
    # Prompt (won't echo)
    return getpass("Enter DB password (will not be shown): ")

def deploy() -> None:
    # 1) Terraform apply
    run(["terraform", "init"], cwd=TERRAFORM_DIR)
    run(["terraform", "fmt", "-recursive"], cwd=TERRAFORM_DIR)
    run(["terraform", "validate"], cwd=TERRAFORM_DIR)
    run(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR)

    # 2) Ansible playbook (init DB + run containers)
    db_password = get_db_password()
    run([
        "ansible-playbook",
        "-i", str(INVENTORY),
        str(PLAYBOOK),
        "-e", f"db_password={db_password}",
    ], cwd=ROOT)

    print("\n✅ Deploy complete.")
    print("Auth:    http://localhost:5000/login")
    print("Catalog: http://localhost:5001/products")

def destroy() -> None:
    # Optional: stop containers (Ansible-created) before terraform destroy
    # (Terraform destroy won't remove containers if you removed docker_container resources.)
    try:
        run(["docker", "rm", "-f", "auth-service", "catalog-service"], cwd=ROOT)
    except subprocess.CalledProcessError:
        pass

    # Terraform destroy for AWS resources + docker network/images (if still managed)
    run(["terraform", "destroy", "-auto-approve"], cwd=TERRAFORM_DIR)
    print("\n🧹 Destroy complete.")

def usage() -> None:
    print("Usage:")
    print("  python3 deploy.py deploy")
    print("  python3 deploy.py destroy")
    print("\nTip: set DB_PASSWORD in your shell to avoid prompts:")
    print("  export DB_PASSWORD='yourpassword'")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"deploy", "destroy"}:
        usage()
        sys.exit(1)

    action = sys.argv[1]
    if action == "deploy":
        deploy()
    else:
        destroy()
