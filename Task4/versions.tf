terraform {
  required_version = ">= 1.5.0"

  required_providers {
    yandex = {
      source  = "registry.terraform.io/yandex-cloud/yandex"
      version = "~> 0.220"
    }
  }
}

provider "yandex" {
  cloud_id                 = var.cloud_id != "" ? var.cloud_id : null
  folder_id                = var.folder_id != "" ? var.folder_id : null
  service_account_key_file = var.service_account_key_file != "" ? pathexpand(var.service_account_key_file) : null
  zone                     = var.zone
}
