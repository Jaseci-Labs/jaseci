# resource "aws_eks_cluster" "zsb-eks" {
#   name     = format("%s-%s", "zsb-eks", local.envsuffix)
#   role_arn = aws_iam_role.zsb-eks-cluster-role.arn

#   # Ensure that IAM Role permissions are created before and deleted after EKS Cluster handling.
#   # Otherwise, EKS will not be able to properly delete EKS managed EC2 infrastructure such as Security Groups.
#   depends_on = [
#     aws_iam_role_policy_attachment.zsb-eks-cluster-role-AmazonEKSClusterPolicy,
#     aws_iam_role_policy_attachment.zsb-eks-cluster-role-AmazonEKSServicePolicy,
#   ]

#   vpc_config {
#     #cluster_security_group_id = aws_security_group.eks-cluster-sg-zsb-cluster.id
#     # endpoint_private_access = false
#     # endpoint_public_access  = true
#     # public_access_cidrs = [ "0.0.0.0/0"]
#     # security_group_ids = [
#     #   aws_security_group.zsb-middleware-eks-cluster.id,
#     # ]
#     subnet_ids = [
#       aws_subnet.zsb-eu-west-2a-public.id,
#       aws_subnet.zsb-eu-west-2b-public.id,
#       aws_subnet.zsb-eu-west-2c-public.id,
#     ]

#   }

#   #Enabled all cluster log types for zsb eks logging
#   enabled_cluster_log_types = [
#     "api",
#     "audit",
#     "authenticator",
#     "controllerManager",
#     "scheduler",
#   ]

#   tags = {
#     "Name" = format("%s-%s", "zsb-middleware", local.envsuffix)
#   }

       
#   #Can be commented if we want to install the latest version
#   version = "1.18"
# }


# #zsb EKS Cluster - Node GROUP
# # terraform import aws_eks_node_group.my_node_group my_cluster:my_node_group
# resource "aws_eks_node_group" "zsb-eks-nodegroup" {
#   cluster_name    = aws_eks_cluster.zsb-eks.name
#   node_group_name = format("%s-%s", "zsb-eks-nodegroup", local.envsuffix)
#   node_role_arn   = aws_iam_role.zsb-eks-node-role.arn
#    subnet_ids      = [
#       "${aws_subnet.zsb-eu-west-2a-public.id}","${aws_subnet.zsb-eu-west-2b-public.id}", "${aws_subnet.zsb-eu-west-2c-public.id}"
#   ]

#   scaling_config {
#     desired_size = 1
#     max_size     = 2
#     min_size     = 1
#   }
#  tags = {
#     format("%s-%s", "kubernetes.io/cluster/zsb-eks", local.envsuffix) = "owned" 
#   }
# instance_types  = ["m4.large"]
#   # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
#   # Otherwise, EKS will not be able to properly delete EC2 Instances and Elastic Network Interfaces.
#   depends_on = [
#     aws_iam_role_policy_attachment.zsb-eks-cluster-role-AmazonEKSWorkerNodePolicy,
#     aws_iam_role_policy_attachment.zsb-eks-node-role-AmazonEKS_CNI_Policy,
#     aws_iam_role_policy_attachment.zsb-eks-node-role-AmazonEC2ContainerRegistryReadOnly,
#     aws_subnet.zsb-eu-west-2a-public,
#     aws_subnet.zsb-eu-west-2b-public,
#     aws_subnet.zsb-eu-west-2c-public

#   ]
# }

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = "1.19"
  subnets         = module.vpc.private_subnets

  tags = {
    "Name" = format("%s-%s", "zsb-eks", local.envsuffix)
  }
  vpc_id = module.vpc.vpc_id

  workers_group_defaults = {
    root_volume_type = "gp2"
  }
  wait_for_cluster_interpreter = ["C:/Program Files/Git/bin/sh.exe", "-c"]
  wait_for_cluster_cmd         = "until curl -sk $ENDPOINT >/dev/null; do sleep 4; done"
  # worker_groups = [
    
  #   {
  #     name                          = "worker-group-1"
  #     instance_type                 = "t2.medium"
  #     additional_userdata           = "echo foo bar"
  #     additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
  #     asg_desired_capacity          = 1
  #   },
  # ]
}

data "aws_eks_cluster" "zsb-eks" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "zsb-eks" {
  name = module.eks.cluster_id
}

resource "aws_eks_node_group" "moolahnodegroup" {
    ami_type        = "AL2_x86_64"
    #arn             = "arn:aws:eks:us-west-2:020711562587:nodegroup/zsb-eks-dev/biggernodepool/7ebc9ca6-1a50-917f-c053-710cf1bdfcd5"
    capacity_type   = "ON_DEMAND"
    cluster_name    = "zsb-eks-dev"
    disk_size       = 20
    #id              = "zsb-eks-dev:biggernodepool"
    instance_types  = [
        "t3.xlarge",
    ]
    labels          = {}
    node_group_name = "biggernodepool"
    node_role_arn   = "arn:aws:iam::020711562587:role/zsb-eks-dev2021042621300107760000000c"
    release_version = "1.19.6-20210504"
 
    #status          = "ACTIVE"
    subnet_ids      = [
        "subnet-0843784107775a5fa",
        "subnet-0aba3f92438d40476",
        "subnet-0d63eb93dd8ad26be",
    ]
    tags            = {}
    tags_all        = {}
    version         = "1.19"

    scaling_config {
        desired_size = 3
        max_size     = 4
        min_size     = 3
    }

    timeouts {}
}
# resource "aws_eks_node_group" "moolahnodegroup" {
#     ami_type        = "AL2_x86_64"
#    # arn             = "arn:aws:eks:us-west-2:020711562587:nodegroup/zsb-eks-dev/nodepoolzsb/78bc99d6-7ec7-0e3b-8a9e-8220543a5c5a"
#     capacity_type   = "ON_DEMAND"
#     cluster_name    = "zsb-eks-dev"
#     disk_size       = 20
#    # id              = "zsb-eks-dev:nodepoolzsb"
#     instance_types  = [
#         "t3.medium",
#     ]
#     labels          = {}
#     node_group_name = "nodepoolzsb"
#     node_role_arn   = "arn:aws:iam::020711562587:role/zsb-eks-dev2021042621300107760000000c"
#     #release_version = "1.18.9-20210501"
  
#    # status          = "ACTIVE"
#     subnet_ids      = [
#         "subnet-0843784107775a5fa",
#         "subnet-0aba3f92438d40476",
#         "subnet-0d63eb93dd8ad26be",
#     ]
#     tags            = {}
#     tags_all        = {}
#     version         = "1.19"

#     scaling_config {
#         desired_size = 1
#         max_size     = 3
#         min_size     = 1
#     }

#     timeouts {}
# }