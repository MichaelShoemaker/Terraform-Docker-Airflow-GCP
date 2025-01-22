import os

# Paths to required files
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
sudo: "ALL=(ALL) NOPASSWD:ALL"
ssh_authorized_keys:
- {ssh_key}

write_files:
- path: /tmp/install_docker.sh
permissions: '0755'
content: |
{script_content.replace('\n', '\n ')}

- path: /tmp/temp_credentials.json
permissions: '0644'
content: |
{service_account.replace('\n', '\n ')}

runcmd:
# Update package lists
- sudo apt-get update

# Clone the Git repository
- if [ ! -d "/home/gary/airflow-docker-compose2025" ]; then
git clone https://github.com/MichaelShoemaker/airflow-docker-compose2025.git /home/gary/airflow-docker-compose2025;
fi

# Ensure directories exist for logs, config, and plugins
- sudo mkdir -p /home/gary/airflow-docker-compose2025/.google/credentials
- sudo mkdir -p /home/gary/airflow-docker-compose2025/logs
- sudo mkdir -p /home/gary/airflow-docker-compose2025/plugins
- sudo mkdir -p /home/gary/airflow-docker-compose2025/config

# Move the temporary credentials file to the Git repository
- sudo mv /tmp/temp_credentials.json /home/gary/airflow-docker-compose2025/.google/credentials/google_credentials.json
- sudo chmod 0644 /home/gary/airflow-docker-compose2025/.google/credentials/google_credentials.json

# Set proper permissions for the directories
- sudo chown -R 1001:1001 /home/gary/airflow-docker-compose2025/dags
- sudo chown -R 1001:1001 /home/gary/airflow-docker-compose2025/logs
- sudo chown -R 1001:1001 /home/gary/airflow-docker-compose2025/plugins
- sudo chown -R 1001:1001 /home/gary/airflow-docker-compose2025/config
- sudo chmod -R 775 /home/gary/airflow-docker-compose2025/dags
- sudo chmod -R 775 /home/gary/airflow-docker-compose2025/logs
- sudo chmod -R 775 /home/gary/airflow-docker-compose2025/plugins
- sudo chmod -R 775 /home/gary/airflow-docker-compose2025/config

# Install Docker using the script
- sudo bash /tmp/install_docker.sh

# Start Docker Compose services
- docker compose -f /home/gary/airflow-docker-compose2025/docker-compose.yml up airflow-init
- sleep 30
- docker compose -f /home/gary/airflow-docker-compose2025/docker-compose.yml up
"""

# Write the cloud-config to a file
output_path = "user-data.yaml"
with open(output_path, "w") as file:
  file.write(cloud_config)

print(f"Cloud-init configuration written to {output_path}")
