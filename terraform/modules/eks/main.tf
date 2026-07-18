# Minimal lab EKS cluster (cost-capped: one managed node).

variable "enable_eks" {
  type    = bool
  default = false
}

variable "environment" {
  type = string
}

variable "subnet_ids" {
  type    = list(string)
  default = []
}

variable "cluster_version" {
  type    = string
  default = "1.32"
}

locals {
  name = "cops-${var.environment}"
}

data "aws_iam_policy_document" "eks_cluster_assume" {
  count = var.enable_eks ? 1 : 0
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "cluster" {
  count              = var.enable_eks ? 1 : 0
  name               = "${local.name}-eks-cluster"
  assume_role_policy = data.aws_iam_policy_document.eks_cluster_assume[0].json
  tags = {
    Project     = "continuityops"
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "cluster_policy" {
  count      = var.enable_eks ? 1 : 0
  role       = aws_iam_role.cluster[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

data "aws_iam_policy_document" "eks_node_assume" {
  count = var.enable_eks ? 1 : 0
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "node" {
  count              = var.enable_eks ? 1 : 0
  name               = "${local.name}-eks-node"
  assume_role_policy = data.aws_iam_policy_document.eks_node_assume[0].json
  tags = {
    Project     = "continuityops"
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "node_worker" {
  count      = var.enable_eks ? 1 : 0
  role       = aws_iam_role.node[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "node_cni" {
  count      = var.enable_eks ? 1 : 0
  role       = aws_iam_role.node[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "node_ecr" {
  count      = var.enable_eks ? 1 : 0
  role       = aws_iam_role.node[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_eks_cluster" "lab" {
  count    = var.enable_eks ? 1 : 0
  name     = local.name
  role_arn = aws_iam_role.cluster[0].arn
  version  = var.cluster_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  tags = {
    Project     = "continuityops"
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy
  ]
}

resource "aws_eks_node_group" "lab" {
  count           = var.enable_eks ? 1 : 0
  cluster_name    = aws_eks_cluster.lab[0].name
  node_group_name = "${local.name}-ng"
  node_role_arn   = aws_iam_role.node[0].arn
  subnet_ids      = var.subnet_ids
  instance_types  = ["t3.small"]
  capacity_type   = "ON_DEMAND"

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  labels = {
    project     = "continuityops"
    environment = var.environment
  }

  tags = {
    Project     = "continuityops"
    Environment = var.environment
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_worker,
    aws_iam_role_policy_attachment.node_cni,
    aws_iam_role_policy_attachment.node_ecr
  ]
}

output "eks_enabled" {
  value = var.enable_eks
}

output "cluster_name" {
  value = try(aws_eks_cluster.lab[0].name, null)
}

output "cluster_endpoint" {
  value = try(aws_eks_cluster.lab[0].endpoint, null)
}

output "cluster_arn" {
  value = try(aws_eks_cluster.lab[0].arn, null)
}
