terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.5.0"
    }
  }
  required_version = ">= 1.4.6"
}

module "vpc" {
  source = "./modules/vpc"

  project_id  = var.project_id
  
}

module "gke" {
  source = "./modules/gke"

  project_id    = var.project_id
  cluster_name  = "airflow-gke-sidtest"
  location      = var.location
  vpc_id        = module.vpc.vpc
  subnet_id     = module.vpc.private_subnets[0]
  gke_num_nodes = var.gke_num_nodes
  machine_type  = var.machine_type

}

module "cloudsql" {
  source = "./modules/cloudsql"

  region            = var.region
  location          = var.location
  instance_name     = var.instance_name
  database_version  = var.database_version
  instance_tier     = var.instance_tier
  disk_space        = var.disk_space
  database_name     = var.database_name
  db_username       = var.db_username
  db_password       = var.db_password
}


# google_storage_bucket
module "google_storage_bucket" {  
  source        = "./modules/bucket"  

  project_id    = var.project_id
  region        = var.region
  location      = var.bucket_location  
  bucket_name   = var.bucket_name
  storage_class = var.storage_class
  environment   = var.environment  
}