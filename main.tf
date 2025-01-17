#You don't really need required_providers for this VM, but it is best pactice :-/
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.51.0"
    }
  }
}


provider "google" {
  #Uncomment the credentials here and in the variables file if you are using a service account json file
  #Insteal of gcloud auth application-default login
  credentials = file(var.credentials)
  project = var.project
  region  = var.region
}

# Read in script file
locals {
  script_content = file("Install_docker.sh")
}

resource "google_compute_instance" "vm_instance" {
  name         = "ubuntu-airflow"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      #Find these in gcloud sdk by running gcloud compute machine-types|grep <what you are looking for e.g. ubuntu>
      image = "ubuntu-2004-focal-v20240307b"
    }
  }

  network_interface {
    network = "default"
    #You need access_config in order to get the public IP printed
    access_config{

    }
  }

  # Use the content of the script file in the metadata_startup_script
metadata = {
  ssh-keys = "${var.user}:${file(var.ssh_key_file)}"
  user-data = <<-EOF
    #!/bin/bash
    sudo apt-get update
    echo '${local.script_content}' > /tmp/install_docker.sh
    chmod +x /tmp/install_docker.sh
    bash /tmp/install_docker.sh
    cd /home/${var.user}
    git clone https://github.com/MichaelShoemaker/airflow-docker-compose2025.git
    cd ./airflow-docker-compose2025
    sudo usermod -aG docker ${var.user}
    newgrp docker
    sleep 10
    sudo docker compose up -d 
  EOF
    }
}

output "public_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
}