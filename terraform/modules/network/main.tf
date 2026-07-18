# Lab VPC for staging / recovery-lab (no NAT Gateway — cost-capped lab).

variable "environment" {
  type = string
}

variable "cidr_block" {
  type    = string
  default = "10.20.0.0/16"
}

variable "enable_network_resources" {
  type    = bool
  default = false
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

locals {
  private_subnet_cidrs = ["10.20.1.0/24", "10.20.2.0/24"]
  public_subnet_cidrs  = ["10.20.101.0/24", "10.20.102.0/24"]
  name_prefix          = "cops-${var.environment}"
}

resource "aws_vpc" "lab" {
  count                = var.enable_network_resources ? 1 : 0
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${local.name_prefix}-vpc"
    Project     = "continuityops"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_internet_gateway" "lab" {
  count  = var.enable_network_resources ? 1 : 0
  vpc_id = aws_vpc.lab[0].id

  tags = {
    Name        = "${local.name_prefix}-igw"
    Project     = "continuityops"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count                   = var.enable_network_resources ? length(local.public_subnet_cidrs) : 0
  vpc_id                  = aws_vpc.lab[0].id
  cidr_block              = local.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index % length(var.azs)]
  map_public_ip_on_launch = true

  tags = {
    Name                                        = "${local.name_prefix}-public-${count.index}"
    Project                                     = "continuityops"
    Environment                                 = var.environment
    "kubernetes.io/role/elb"                    = "1"
    "kubernetes.io/cluster/${local.name_prefix}" = "shared"
  }
}

resource "aws_subnet" "private" {
  count             = var.enable_network_resources ? length(local.private_subnet_cidrs) : 0
  vpc_id            = aws_vpc.lab[0].id
  cidr_block        = local.private_subnet_cidrs[count.index]
  availability_zone = var.azs[count.index % length(var.azs)]

  tags = {
    Name                                        = "${local.name_prefix}-private-${count.index}"
    Project                                     = "continuityops"
    Environment                                 = var.environment
    "kubernetes.io/role/internal-elb"           = "1"
    "kubernetes.io/cluster/${local.name_prefix}" = "shared"
  }
}

resource "aws_route_table" "public" {
  count  = var.enable_network_resources ? 1 : 0
  vpc_id = aws_vpc.lab[0].id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab[0].id
  }

  tags = {
    Name        = "${local.name_prefix}-public-rt"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "public" {
  count          = var.enable_network_resources ? length(aws_subnet.public) : 0
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public[0].id
}

output "network_boundary" {
  value = {
    cidr                 = var.cidr_block
    private_subnet_cidrs = local.private_subnet_cidrs
    public_subnet_cidrs  = local.public_subnet_cidrs
    multi_account        = false
    enable_guard         = var.enable_network_resources
    vpc_id               = try(aws_vpc.lab[0].id, null)
    public_subnet_ids    = try(aws_subnet.public[*].id, [])
    private_subnet_ids   = try(aws_subnet.private[*].id, [])
    note                 = var.enable_network_resources ? "Live lab VPC (no NAT)" : "Designed only; enable_network_resources=false"
  }
}
