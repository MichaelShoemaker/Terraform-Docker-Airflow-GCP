# Terraform-Docker-Airflow-GCP
Terraform Files to Create a GCP VM Install Docker Docker-Compose and Run Airflow


## Create a Project in GCP
![til](./images/CreateProject.gif)

## Create a Service Account and Download the Key
Create a Service Account and give it Compute Engine Admin Permissions<br>
Generate and download a key for the Service Account</br>
![til](./images/ServiceAccount.gif)

Create a ./google directory and add your .json key there<br>
Name it terra-airflow or update the varaibles.tf file variable</br>
![til](./images/AddServiceAccount.gif)

## Update the Variables.tf File 
Update the variables in variables.tf to match your project.<br>
A good way to do this is to look at the Dashboard for the project name<br>
Go to Compute Engine and click the Create Instance button.<br>
The default shown for Region and Zone are most likely what you want to use.</br>
![til](./images/SetVariables.gif)