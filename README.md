# Terraform-Docker-Airflow-GCP
Terraform Files to Create a GCP VM Install Docker Docker-Compose and Run Airflow


## Create a Project in GCP


## Create a Service Account and Download the Key
Create a Service Account and give it Compute Engine Admin Permissions
Generate and download a key for the Service Account</br>
![til](./images/ServiceAccount.gif)

Create a ./google directory and add your .json key there
Name it terra-airflow or update the varaibles.tf file variable</br>
![til](./images/AddServiceAccount.gif)