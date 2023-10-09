project_id = "wizeline-deb-capstone"
region     = "us-central1"
location     = "us-central1-b"

#GKE
gke_num_nodes = 2
machine_type  = "n1-standard-2"

#CloudSQL
instance_name     = "wizeline-bootcamp"
database_version  = "POSTGRES_12"
instance_tier     = "db-f1-micro"
disk_space        = 10
database_name     = "capstone"
db_username       = "sisoe"
db_password       = "A6dVuPw$NFBVbFI"

#Bucket
bucket_location = "US"