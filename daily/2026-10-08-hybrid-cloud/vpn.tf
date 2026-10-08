# Day 01 — Hybrid connectivity: AWS Site-to-Site VPN
# Links your on-premises data center to a VPC in ~30 lines.
# Usage: terraform init && terraform apply -var="onprem_public_ip=203.0.113.10"

variable "onprem_public_ip" {
  description = "Public IP of your on-premises VPN device"
  type        = string
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags                 = { Name = "hybrid-vpc" }
}

resource "aws_vpn_gateway" "this" {
  vpc_id          = aws_vpc.main.id
  amazon_side_asn = 64512
  tags            = { Name = "hybrid-vpn-gw" }
}

resource "aws_customer_gateway" "datacenter" {
  bgp_asn    = 65000
  ip_address = var.onprem_public_ip
  type       = "ipsec.1"
  tags       = { Name = "onprem-dc" }
}

resource "aws_vpn_connection" "hybrid" {
  vpn_gateway_id      = aws_vpn_gateway.this.id
  customer_gateway_id = aws_customer_gateway.datacenter.id
  type                = "ipsec.1"
  static_routes_only  = true
  tags                = { Name = "hybrid-tunnel" }
}

resource "aws_vpn_connection_route" "onprem" {
  vpn_connection_id      = aws_vpn_connection.hybrid.id
  destination_cidr_block = "192.168.0.0/16" # your data-center subnet
}

output "tunnel1_status" {
  description = "Check this after apply — both tunnels should be UP"
  value       = aws_vpn_connection.hybrid.tunnel1_status
}
