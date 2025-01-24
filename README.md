# Terraform-Docker-Airflow-GCP
Terraform Files to Create a GCP VM Install Docker Docker-Compose and Run Airflow

## Walkthrough Video for Setup
[![Setup Walkthrough](https://img.youtube.com/vi/HgCRclidDOQ/0.jpg)](https://www.youtube.com/watch?v=HgCRclidDOQ)


## Create a Project in GCP
![til](./images/CreateProject.gif)

## Create a Service Account and Download the Key
Create a Service Account and give it Compute Engine Admin Permissions<br>
Generate and download a key for the Service Account</br>

Note: The variables.tf files are looking for a key titled **terra-airflow.json** in a .google directory in the root of the projects file structure.

![til](./images/ServiceAccount.gif)

Create a ./google directory and add your .json key there<br>
Name it terra-airflow or update the varaibles.tf file variable</br>
![til](./images/AddServiceAccount.gif)

## Update the Variables.tf File 
Update the variables in variables.tf to match your project.<br><br>
A good way to do this is to look at the Dashboard for the project name<br><br>
Go to Compute Engine and click the Create Instance button.<br><br>
The default shown for Region and Zone are most likely what you want to use.</br><br>
![til](./images/SetVariables.gif)


## Generate an SSH Key Pair
<br>

```bash
ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME
```

The files as is will be looking for a private and public key pair with the name "GCP" in your users .ssh directoy.<br>


## Create Service Account for Airflow
You will now need to generate a Service Account with permissions to upload to a GCP Bucket.
![til](./images/gsc_servAcct.png)

Create a key file for the service acount and place it at **.google/credentials/google_credentials.json**
![til](./images/google_credentials.png)

## Deploy to GCP
From either the<br>
file_user-script<br>
or
inline_user-script<br>
directories run<br>
```bash
terraform plan
```
to check for errors<br>
```bash
terraform apply
```
to deploly to GCP
