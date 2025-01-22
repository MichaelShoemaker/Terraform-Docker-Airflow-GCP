
variable "credentials" {
  description = "My Credentials"
  default     = "../.google/terra-airflow.json"
}


variable "project" {
  description = "Project"
  default     = "airflow-test-447115"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "zone" {
    description = "Zone"
    default = "us-central1-c"
}

variable "image" {
    description = "Machine Image"
    default = "ubuntu-2004-focal-v20250111"
}

variable "user"{
    description = "User for maching"
    default = "gary"
}

variable "ssh_key_file" {
  description = "Path to the SSH public key file"
  default     = "~/.ssh/gcp.pub" 

}