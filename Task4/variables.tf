variable "cloud_id" {
  description = "Yandex Cloud ID. Keep empty to use YC_CLOUD_ID or the active provider profile."
  type        = string
  default     = ""
}

variable "folder_id" {
  description = "Yandex Cloud folder ID. Keep empty to use YC_FOLDER_ID or the active provider profile."
  type        = string
  default     = ""
}

variable "service_account_key_file" {
  description = "Path to a service-account key outside the repository. Keep empty to use YC_SERVICE_ACCOUNT_KEY_FILE."
  type        = string
  default     = ""
  sensitive   = true
}

variable "project_name" {
  description = "Human-readable project name exposed by the demo health page."
  type        = string
  default     = "Future 2.0 Data Portal"
}

variable "name_prefix" {
  description = "Prefix for cloud resource names."
  type        = string
  default     = "future-2-0"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,30}$", var.name_prefix))
    error_message = "name_prefix must start with a lowercase letter and contain 3-31 lowercase letters, digits or hyphens."
  }
}

variable "environment" {
  description = "Environment label."
  type        = string
  default     = "demo"
}

variable "zone" {
  description = "Yandex Cloud availability zone."
  type        = string
  default     = "ru-central1-a"
}

variable "subnet_cidr" {
  description = "IPv4 CIDR of the application subnet."
  type        = string
  default     = "10.42.10.0/24"

  validation {
    condition     = can(cidrhost(var.subnet_cidr, 10))
    error_message = "subnet_cidr must be a valid IPv4 CIDR."
  }
}

variable "http_cidrs" {
  description = "CIDRs allowed to access the demo HTTP endpoint. Production must use an ingress load balancer and private backends."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "admin_cidrs" {
  description = "CIDRs allowed to connect over SSH. Empty by default: no SSH ingress."
  type        = list(string)
  default     = []
}

variable "enable_nat" {
  description = "Allocate a public NAT address to the demo VM. Production backends should be private."
  type        = bool
  default     = true
}

variable "image_family" {
  description = "Image family from the standard-images folder."
  type        = string
  default     = "ubuntu-2204-lts"
}

variable "platform_id" {
  description = "Yandex Compute Cloud platform."
  type        = string
  default     = "standard-v2"
}

variable "vm_cores" {
  description = "Virtual CPU count for the pilot VM."
  type        = number
  default     = 2
}

variable "vm_core_fraction" {
  description = "Baseline vCPU performance percentage for the low-load pilot."
  type        = number
  default     = 20
}

variable "vm_memory_gb" {
  description = "RAM size in GiB."
  type        = number
  default     = 2
}

variable "disk_type" {
  description = "Disk type. network-hdd minimizes the cost of a short-lived pilot."
  type        = string
  default     = "network-hdd"
}

variable "boot_disk_size_gb" {
  description = "Boot disk size in GiB."
  type        = number
  default     = 10
}

variable "data_disk_size_gb" {
  description = "Attached data disk size in GiB."
  type        = number
  default     = 10
}

variable "preemptible" {
  description = "Use a preemptible instance for the disposable validation environment."
  type        = bool
  default     = true
}
