output "network_id" {
  description = "ID of the Terraform-managed VPC network."
  value       = yandex_vpc_network.portal.id
}

output "subnet_id" {
  description = "ID of the Terraform-managed subnet."
  value       = yandex_vpc_subnet.portal.id
}

output "security_group_id" {
  description = "ID of the Terraform-managed security group."
  value       = yandex_vpc_security_group.portal.id
}

output "instance_id" {
  description = "ID of the demo VM."
  value       = yandex_compute_instance.portal.id
}

output "instance_internal_ip" {
  description = "Private address of the demo VM."
  value       = yandex_compute_instance.portal.network_interface[0].ip_address
}

output "instance_external_ip" {
  description = "Public NAT address of the demo VM, if NAT is enabled."
  value       = try(yandex_compute_instance.portal.network_interface[0].nat_ip_address, null)
}

output "data_disk_id" {
  description = "ID of the attached data disk."
  value       = yandex_compute_disk.portal_data.id
}

output "health_url" {
  description = "Demo endpoint created by cloud-init."
  value       = var.enable_nat ? "http://${yandex_compute_instance.portal.network_interface[0].nat_ip_address}/" : null
}
