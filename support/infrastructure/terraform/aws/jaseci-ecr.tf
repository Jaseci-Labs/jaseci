#  ECR
resource "aws_ecr_repository" "zsb-ECR" {
  name                 = format("%s-%s", "zsb-ecr", local.envsuffix)
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }
   tags = {
    "Name" = format("%s-%s", "zsb-ECR", local.envsuffix)
  }
}