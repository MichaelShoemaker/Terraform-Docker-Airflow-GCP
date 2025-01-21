import os

ssh_key_path = "~/.ssh/gcp.pub"
script_content_path = "Install_docker.sh"
service_account_path = ".google/credentials/google_credentials.json"

# Read file contents
with open(os.path.expanduser(ssh_key_path), "r") as ssh_file:
    ssh_key = ssh_file.read().strip()

with open(script_content_path, "r") as script_file:
    script_content = script_file.read().strip()

with open(service_account_path, "r") as sa_file:
    service_account = sa_file.read().strip()

# Generate the user-data.yaml
cloud_config = f"""#cloud-config

users:
  - name: gary
    groups: sudo, docker
    shell: /bin/bash
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    ssh_authorized_keys:
      - {ssh_key}

write_files:
  - path: /tmp/install_docker.sh
    permissions: '0755'
    content: |
{script_content.replace('\n', '\n      ')}

  - path: /home/gary/airflow-docker-compose2025/.google/credentials/google_credentials.json
    permissions: '0755'
    owner: gary:gary
    content: |
{service_account.replace('\n', '\n      ')}

runcmd:
  - sudo apt-get update
  - sudo mkdir -p /home/gary/.google/credentials
  - sudo chmod -R 755 /home/gary/.google

  - cd /home/gary
  - git clone https://github.com/MichaelShoemaker/airflow-docker-compose2025.git
  - sudo mkdir -p /home/gary/airflow-docker-compose2025/.google/credentials
  - sudo chmod -R 755 /home/gary/airflow-docker-compose2025/.google

  - sudo mkdir -p /home/gary/airflow-docker-compose2025/dags /home/gary/airflow-docker-compose2025/logs /home/gary/airflow-docker-compose2025/plugins /home/gary/airflow-docker-compose2025/config
  - sudo chown -R 1001:1001 /home/gary/airflow-docker-compose2025/dags /home/gary/airflow-docker-compose2025/logs /home/gary/airflow-docker-compose2025/plugins /home/gary/airflow-docker-compose2025/config
  - sudo chmod -R 775 /home/gary/airflow-docker-compose2025/dags /home/gary/airflow-docker-compose2025/logs /home/gary/airflow-docker-compose2025/plugins /home/gary/airflow-docker-compose2025/config

  - sudo usermod -aG docker gary
  - newgrp docker
  - docker compose -f /home/gary/airflow-docker-compose2025/docker-compose.yml up airflow-init
  - sleep 30
  - docker compose -f /home/gary/airflow-docker-compose2025/docker-compose.yml up
"""

# Write the cloud-config to a file
output_path = "user-data.yaml"
with open(output_path, "w") as file:
    file.write(cloud_config)

print(f"Cloud-init configuration written to {output_path}")
