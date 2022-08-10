resource "kubernetes_config_map" "aws_auth"{
 data = {
           "mapRoles" = <<-EOT
                - "groups":
                  - "system:bootstrappers"
                  - "system:nodes"
                  "rolearn": "arn:aws:iam::020711562587:role/zsb-eks-dev2021042621300107760000000c"
                  "username": "system:node:{{EC2PrivateDNSName}}"  
            EOT
        } 
      # id   = "default/aws-auth"

       metadata {
           #generation       = 0
           name             = "aws-auth"
           namespace        = "default"
          # resource_version = "1300506"
          # uid              = "eaa91f81-9abb-467a-8e97-b50a65f100c4"
        }
    }
