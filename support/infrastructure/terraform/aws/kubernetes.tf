provider "kubernetes" {
  host                   = data.aws_eks_cluster.zsb-eks.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.zsb-eks.certificate_authority.0.data)
  exec {
    api_version = "client.authentication.k8s.io/v1alpha1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      data.aws_eks_cluster.zsb-eks.name
    ]
  }
}