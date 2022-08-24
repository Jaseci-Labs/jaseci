module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = local.clusterversion
  subnets         = module.vpc.private_subnets

  tags = {
    "Name" = format("%s-%s", "jaseci-eks", local.envsuffix)
  }
  vpc_id = module.vpc.vpc_id

  workers_group_defaults = {
    root_volume_type = "gp2"
  }
  # wait_for_cluster_interpreter = ["C:/Program Files/Git/bin/sh.exe", "-c"]
  # wait_for_cluster_cmd         = "until curl -sk $ENDPOINT >/dev/null; do sleep 4; done"
  worker_groups = [
    
    {
      name                          = format("%s-%s", "jaseci-eks-wg", local.envsuffix)
      instance_type                 = local.instance_type
      additional_userdata           = ""
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
      asg_desired_capacity          = 2
    },
  ]
}

data "aws_eks_cluster" "zsb-eks" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "zsb-eks" {
  name = module.eks.cluster_id
}

# resource "aws_eks_node_group" "moolahnodegroup" {
#     ami_type        = "AL2_x86_64"
#     #arn             = "arn:aws:eks:us-west-2:020711562587:nodegroup/zsb-eks-dev/biggernodepool/7ebc9ca6-1a50-917f-c053-710cf1bdfcd5"
#     capacity_type   = "ON_DEMAND"
#     cluster_name    = format("%s-%s", "jaseci-eks", local.envsuffix)
#     disk_size       = 20
#     #id              = "zsb-eks-dev:biggernodepool"
#     instance_types  = [
#         "t3.xlarge",
#     ]
#     labels          = {}
#     node_group_name = "biggernodepool"
#     node_role_arn   = "arn:aws:iam::020711562587:role/zsb-eks-dev2021042621300107760000000c"
#     release_version = "1.19.6-20210504"
 
#     #status          = "ACTIVE"
#     subnet_ids      = [
#         "subnet-0843784107775a5fa",
#         "subnet-0aba3f92438d40476",
#         "subnet-0d63eb93dd8ad26be",
#     ]
#     tags            = {}
#     tags_all        = {}
#     version         = "1.19"

#     scaling_config {
#         desired_size = 3
#         max_size     = 4
#         min_size     = 3
#     }

#     timeouts {}
# }