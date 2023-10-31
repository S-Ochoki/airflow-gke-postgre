variable "project_id" {
  description   = "The Project ID in which will be deployed the services"
}

variable "location" {
  description   = "General location for deployments"
}

variable "region" {
  description   = "The region in which the GCP bucket will be created."
}

variable "bucket_name" {
  description   = "The name of the GCP bucket to create."
}

variable "storage_class" {
  description   = "Storage class for the bucket"
}

variable "environment" {
  description   = "Environment definition"
}