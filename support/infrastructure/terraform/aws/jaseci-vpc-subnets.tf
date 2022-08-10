# # #zsb VPC Subnets

# # #Public 1A
# resource "aws_subnet" "zsb-eu-west-2a-public" {
#   availability_zone               = "eu-west-2a"
#   cidr_block                      = "172.20.48.0/20"
#   ipv6_cidr_block                 = null
#   map_public_ip_on_launch         = true
#   outpost_arn                     = ""
#   assign_ipv6_address_on_creation = false
#   tags = {
#     "Name" = "zsb-eu-west-2a-public"
#   }
#   vpc_id = aws_vpc.zsb-vpc.id
# }

# # #Private 1A
# resource "aws_subnet" "zsb-eu-west-2a-private" {
#   availability_zone               = "eu-west-2a"
#   cidr_block                      = "172.20.16.0/20"
#   ipv6_cidr_block                 = null
#   map_public_ip_on_launch         = true
#   outpost_arn                     = ""
#   assign_ipv6_address_on_creation = false
#   tags = {
#     "Name"                                 = "zsb-eu-west-2a-private"
#     format("%s-%s", "kubernetes.io/cluster/zsb-eks", local.envsuffix) = "shared"
#     "kubernetes.io/role/internal-elb"      = "1" #For Private EKS launching ELB
#   }
#   vpc_id = aws_vpc.zsb-vpc.id
# }

# # #Private 1B
# resource "aws_subnet" "zsb-eu-west-2b-public" {
#   availability_zone               = "eu-west-2b"
#   cidr_block                      = "172.20.96.0/20"
#   ipv6_cidr_block                 = null
#   map_public_ip_on_launch         = true
#   outpost_arn                     = ""
#   assign_ipv6_address_on_creation = false
#   tags = {
#     "Name"                                 = "zsb-eu-west-2b-public"
#     format("%s-%s", "kubernetes.io/cluster/zsb-eks", local.envsuffix) = "shared"
#     "kubernetes.io/role/internal-elb"      = "1" #For Private EKS launching ELB
#   }
#   vpc_id = aws_vpc.zsb-vpc.id
# }

# # #Private 1C
# resource "aws_subnet" "zsb-eu-west-2c-public" {
#   availability_zone               = "eu-west-2c"
#   cidr_block                      = "172.20.32.0/20"
#   ipv6_cidr_block                 = null
#   map_public_ip_on_launch         = true
#   outpost_arn                     = ""
#   assign_ipv6_address_on_creation = false
#   tags = {
#     "Name"                                 = "zsb-eu-west-2c-public"
#     format("%s-%s", "kubernetes.io/cluster/zsb-eks", local.envsuffix) = "shared"
#     "kubernetes.io/role/internal-elb"      = "1" #For Private EKS launching ELB
#   }
#   vpc_id = aws_vpc.zsb-vpc.id
# }