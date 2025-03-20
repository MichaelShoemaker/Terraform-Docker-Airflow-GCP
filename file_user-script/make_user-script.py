import os

# Paths to required files
ssh_key_path = os.path.expanduser("~/.ssh/gcp.pub")
script_content_path = "Install_docker.sh"
service_account_path = ".google/credentials/google_credentials.json"

# Read file contents
with open(ssh_key_path, "r") as ssh_file:
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
    sudo: "ALL=(ALL) NOPASSWD:ALL"
    ssh_authorized_keys:
      - {ssh_key}

write_files:
  - path: /tmp/install_docker.sh
    permissions: '0755'
    owner: root:root
    content: |
      {script_content.replace('\n', '\n      ')}  # Properly indented

  - path: /tmp/temp_credentials.json
    permissions: '0644'
    owner: root:root
    content: |
      {service_account.replace('\n', '\n      ')}  # Properly indented

runcmd:
  - sudo apt-get update -y

  # Clone Git Repository if not already present
  - if [ ! -d "/home/gary/airflow-docker-compose2025" ]; then 
      git clone https://github.com/MichaelShoemaker/airflow-docker-compose2025.git /home/gary/airflow-docker-compose2025; 
    fi

  # Ensure necessary directories exist
  - mkdir -p /home/gary/airflow-docker-compose2025/.google/credentials
  - mkdir -p /home/gary/airflow-docker-compose2025/logs
  - mkdir -p /home/gary/airflow-docker-compose2025/plugins
  - mkdir -p /home/gary/airflow-docker-compose2025/config

  # Move credentials
  - mv /tmp/temp_credentials.json /home/gary/airflow-docker-compose2025/.google/credentials/google_credentials.json
  - chmod 0644 /home/gary/airflow-docker-compose2025/.google/credentials/google_credentials.json

  # Set proper permissions for directories
  - chown -R 1001:1001 /home/gary/airflow-docker-compose2025/dags
  - chown -R 1001:1001 /home/gary/airflow-docker-compose2025/logs
  - chown -R 1001:1001 /home/gary/airflow-docker-compose2025/plugins
  - chown -R 1001:1001 /home/gary/airflow-docker-compose2025/config
  - chmod -R 775 /home/gary/airflow-docker-compose2025/dags
  - chmod -R 775 /home/gary/airflow-docker-compose2025/logs
  - chmod -R 775 /home/gary/airflow-docker-compose2025/plugins
  - chmod -R 775 /home/gary/airflow-docker-compose2025/config

  # Install Docker
  - bash /tmp/install_docker.sh

  # Start Docker Compose services
  - docker compose -f /home/gary/airflow-docker-compose2025/docker-compose.yml up airflow-init
  - sleep 30
  - docker compose -f /home/gary/airflow-docker-compose2025/docker-compose.yml up
"""

# Write the cloud-config to a file
output_path = "user-data.yaml"
with open(output_path, "w") as file:
    file.write(cloud_config)

print(f"Fixed Cloud-init configuration written to {output_path}")
