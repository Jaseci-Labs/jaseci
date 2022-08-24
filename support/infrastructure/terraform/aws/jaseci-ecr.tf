#  ECR
resource "aws_ecr_repository" "zsb-ECR" {
  name                 = format("%s-%s", "jaseci-ecr", local.envsuffix)
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }
   tags = {
    "Name" = format("%s-%s", "jaseci-ECR", local.envsuffix)
  }
}