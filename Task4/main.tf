data "yandex_compute_image" "ubuntu" {
  family    = var.image_family
  folder_id = "standard-images"
}

resource "yandex_vpc_network" "portal" {
  name        = "${var.name_prefix}-network"
  description = "Network for the Future 2.0 self-service data portal pilot"

  labels = local.common_labels
}

resource "yandex_vpc_subnet" "portal" {
  name           = "${var.name_prefix}-subnet"
  description    = "Application subnet managed by Terraform"
  zone           = var.zone
  network_id     = yandex_vpc_network.portal.id
  v4_cidr_blocks = [var.subnet_cidr]

  labels = local.common_labels
}

resource "yandex_vpc_security_group" "portal" {
  name        = "${var.name_prefix}-sg"
  description = "Least-privilege ingress for the pilot portal"
  network_id  = yandex_vpc_network.portal.id

  ingress {
    protocol       = "TCP"
    description    = "HTTP health page"
    port           = 80
    v4_cidr_blocks = var.http_cidrs
  }

  dynamic "ingress" {
    for_each = length(var.admin_cidrs) > 0 ? [1] : []

    content {
      protocol       = "TCP"
      description    = "Administrative SSH from explicitly approved networks"
      port           = 22
      v4_cidr_blocks = var.admin_cidrs
    }
  }

  egress {
    protocol       = "ANY"
    description    = "Outbound package installation and managed service access"
    from_port      = 0
    to_port        = 65535
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  labels = local.common_labels
}

resource "yandex_compute_disk" "portal_data" {
  name        = "${var.name_prefix}-data"
  description = "Separate data disk: lifecycle is independent from the boot disk"
  type        = var.disk_type
  zone        = var.zone
  size        = var.data_disk_size_gb

  labels = local.common_labels
}

resource "yandex_compute_instance" "portal" {
  name                      = "${var.name_prefix}-vm"
  hostname                  = "${var.name_prefix}-vm"
  description               = "Future 2.0 self-service data portal IaaS pilot"
  platform_id               = var.platform_id
  zone                      = var.zone
  allow_stopping_for_update = true

  resources {
    cores         = var.vm_cores
    core_fraction = var.vm_core_fraction
    memory        = var.vm_memory_gb
  }

  scheduling_policy {
    preemptible = var.preemptible
  }

  boot_disk {
    auto_delete = true

    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = var.boot_disk_size_gb
      type     = var.disk_type
    }
  }

  secondary_disk {
    disk_id     = yandex_compute_disk.portal_data.id
    auto_delete = true
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.portal.id
    nat                = var.enable_nat
    security_group_ids = [yandex_vpc_security_group.portal.id]
  }

  metadata = {
    serial-port-enable = "1"
    user-data = templatefile("${path.module}/cloud-init.yaml.tftpl", {
      project_name = var.project_name
    })
  }

  labels = local.common_labels
}

locals {
  common_labels = {
    project     = "future-2-0"
    environment = var.environment
    managed-by  = "terraform"
    owner       = "data-platform"
  }
}
