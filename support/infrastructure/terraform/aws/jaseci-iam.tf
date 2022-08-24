# #EKS Role
# resource "aws_iam_role" "zsb-eks-cluster-role" {
#   name = "zsb-eks-cluster-role"
#   assume_role_policy = jsonencode(
#     {
#       Statement = [
#         {
#           Action = "sts:AssumeRole"
#           Effect = "Allow"
#           Principal = {
#             Service = "eks.amazonaws.com"           
#           }
#         },
#       ]
#       Version = "2012-10-17"
#     }
#   )

#   force_detach_policies = false
#   path                  = "/"
#   description           = "zsb: Allows EKS to manage clusters on your behalf."
#   max_session_duration  = 3600
#   tags                  = {}
# }

# #zsb Profile Service EKS Node Role
# resource "aws_iam_role" "zsb-eks-node-role" {
#   name = "zsb-eks-node-role"
#   assume_role_policy = jsonencode(
#     {
#       Statement = [
#         {
#           Action = "sts:AssumeRole"
#           Effect = "Allow"
#           Principal = {
#             Service = "ec2.amazonaws.com"
#           }
#         },
#       ]
#       Version = "2012-10-17"
#     }
#   )
#   force_detach_policies = false
#   path                  = "/"
#   description           = "zsb: EKS Node Role"
#   max_session_duration  = 3600
#   tags                  = {}
# }
# resource "aws_iam_instance_profile" "zsb-eks-node-role" {
#   name = "zsb-eks-node-role"
#   path = "/"
#   role = "zsb-eks-node-role"
# }

# ## IAM Attached Policies for ROLES ###
# resource "aws_iam_role_policy_attachment" "zsb-eks-cluster-role-AmazonEKSClusterPolicy" {
#   role       = aws_iam_role.zsb-eks-cluster-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-cluster-role-AmazonEKSServicePolicy" {
#   role       = aws_iam_role.zsb-eks-cluster-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-cluster-role-AmazonEKSWorkerNodePolicy" {
#   role       = aws_iam_role.zsb-eks-cluster-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
# }
# resource "aws_iam_role_policy_attachment" "zsb-eks-cluster-role-AmazonEC2ContainerRegistryReadOnly" {
#   role       = aws_iam_role.zsb-eks-cluster-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
# }
# resource "aws_iam_role_policy_attachment" "zsb-eks-cluster-role-AmazonEKSVPCResourceController" {
#   role       = aws_iam_role.zsb-eks-cluster-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-node-role-SecretsManagerReadWrite" {
#   role       = aws_iam_role.zsb-eks-node-role.name
#   policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-node-role-AmazonEKSWorkerNodePolicy" {
#   role       = aws_iam_role.zsb-eks-node-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-node-role-AmazonEC2ContainerRegistryReadOnly" {
#   role       = aws_iam_role.zsb-eks-node-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-node-role-AmazonSSMFullAccess" {
#   role       = aws_iam_role.zsb-eks-node-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSSMFullAccess"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-node-role-AmazonEKS_CNI_Policy" {
#   role       = aws_iam_role.zsb-eks-node-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
# }

# resource "aws_iam_role_policy_attachment" "zsb-eks-node-role-AmazonS3FullAccess" {
#   role       = aws_iam_role.zsb-eks-node-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
# }


resource "aws_iam_policy" "cluster_elb_sl_role_creation" {

    description = "Permissions for EKS to create AWSServiceRoleForElasticLoadBalancing service-linked role"
    
    name        = "jaseci-eks-dev-elb-sl-role-creation20210426211834225900000001"
    path        = "/"
    policy      = jsonencode(
        {
            Statement = [
                {
                    Action   = [
                        "ec2:DescribeInternetGateways",
                        "ec2:DescribeAddresses",
                        "ec2:DescribeAccountAttributes",
                    ]
                    Effect   = "Allow"
                    Resource = "*"
                    Sid      = ""
                },
            ]
            Version   = "2012-10-17"
        }
    )
  
        tags    = {
          "Name" = "jaseci-eks-dev"
        }
       tags_all    = {
           "Name" = "jaseci-eks-dev"
        }
}