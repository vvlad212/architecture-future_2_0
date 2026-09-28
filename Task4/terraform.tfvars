# Account identifiers and credentials are intentionally not committed.
# Authentication comes from YC_CLOUD_ID, YC_FOLDER_ID and
# YC_SERVICE_ACCOUNT_KEY_FILE (or from an active provider profile).
cloud_id                 = ""
folder_id                = ""
service_account_key_file = ""

project_name      = "Future 2.0 Data Portal"
name_prefix       = "future-2-0"
environment       = "demo"
zone              = "ru-central1-a"
subnet_cidr       = "10.42.10.0/24"
http_cidrs        = ["0.0.0.0/0"]
admin_cidrs       = []
enable_nat        = true
image_family      = "ubuntu-2204-lts"
platform_id       = "standard-v2"
vm_cores          = 2
vm_core_fraction  = 20
vm_memory_gb      = 2
disk_type         = "network-hdd"
boot_disk_size_gb = 10
data_disk_size_gb = 10
preemptible       = true
