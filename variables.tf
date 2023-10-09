# wizeline-deb-capstone
variable "project_id" {
  description = "wizeline-deb-capstone"
}

variable "region" {
  description = "us-central1"
}

variable "location" {
  description = "us-central1-b"
}


# GKE
variable "gke_num_nodes" {
  default     = 2
  description = "number of gke nodes"
}

variable "machine_type" {
  type = string
  default = "n1-standard-2"
}


# CloudSQL
variable "instance_name" {
  description = "Name for the sql instance database"
  default     = "wizeline-bootcamp"
}

variable "database_version" {
  description = "The MySQL, PostgreSQL or SQL Server (beta) version to use. "
  default     = "POSTGRES_12"
}

variable "instance_tier" {
  description = "Sql instance tier"
  default     = "db-f1-micro"
}

variable "disk_space" {
  description = "Size of the disk in the sql instance"
  default     = 10
}

variable "database_name" {
  description = "Name for the database to be created"
  default     = "capstone"
}

variable "db_username" {
  description = "Username credentials for root user"
  default     = "sisoe"
}
variable "db_password" {
  description = "Password credentials for root user"
  default     = "A6dVuPw$NFBVbFI"
}

# Cloud bucket
variable "bucket_name" {
  description = "Name of the Google Cloud Storage bucket"
  default = "wizeline_bootcamp_bucket"
}

variable "storage_class" {
  description = "Storage class for the bucket (e.g., 'STANDARD', 'NEARLINE', 'COLDLINE')"
  default     = "STANDARD"
}

variable "environment" {
  type          = string
  default       = "dev"
  description   = "Environment definition"
}

variable "bucket_location" {
  description = "US"
}
