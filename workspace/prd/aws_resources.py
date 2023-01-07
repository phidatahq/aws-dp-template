from phidata.infra.aws.resource.group import (
    AcmCertificate,
    CloudFormationStack,
    EksCluster,
    EksKubeconfig,
    EksNodeGroup,
    AwsResourceGroup,
    S3Bucket,
)
from typing_extensions import Literal

from workspace.settings import (
    prd_domain,
    prd_key,
    prd_tags,
    private_subnets,
    ws_dir_path,
)

#
# -*- AWS resources
#

# -*- Settings
aws_skip_create: bool = False
# Prevents deletion when running `phi ws down`
aws_skip_delete: bool = False
aws_wait_for_create: bool = True
aws_wait_for_delete: bool = False

# -*- S3 buckets
# S3 bucket for storing logs
prd_logs_s3_bucket = S3Bucket(
    name=f"{prd_key}-logs",
    acl="private",
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)
# S3 bucket for storing data
prd_data_s3_bucket = S3Bucket(
    name=f"{prd_key}-data",
    acl="private",
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- VPC stack for EKS
prd_vpc_stack = CloudFormationStack(
    name=f"{prd_key}-vpc",
    template_url="https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml",
    tags=prd_tags,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- EKS settings
# Node Group label for Services
services_ng_label = {
    "app_type": "service",
}
# Node Group label for Workers
workers_ng_label = {
    "app_type": "worker",
}
# How to distribute pods across EKS nodes
# "kubernetes.io/hostname" means spread across nodes
topology_spread_key: str = "kubernetes.io/hostname"
topology_spread_max_skew: int = 2
topology_spread_when_unsatisfiable: Literal[
    "DoNotSchedule", "ScheduleAnyway"
] = "DoNotSchedule"

# -*- EKS cluster
prd_eks_cluster = EksCluster(
    name=f"{prd_key}-cluster",
    # Add subnets and security groups.
    resources_vpc_config={
        "subnetIds": private_subnets,
    },
    # To use the prd_vpc_stack from above,
    # uncomment the line below and comment out the resources_vpc_config above
    # vpc_stack=prd_vpc_stack,
    tags=prd_tags,
    # Manage kubeconfig separately using an EksKubeconfig resource
    manage_kubeconfig=False,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- EKS Kubeconfig
prd_eks_kubeconfig = EksKubeconfig(eks_cluster=prd_eks_cluster)

# -*- EKS cluster nodegroup for running core services
prd_services_eks_nodegroup = EksNodeGroup(
    name=f"{prd_key}-services-ng",
    min_size=2,
    max_size=5,
    desired_size=2,
    disk_size=64,
    instance_types=["m5.large"],
    eks_cluster=prd_eks_cluster,
    # Add the services label to the nodegroup
    labels=services_ng_label,
    tags=prd_tags,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- EKS cluster nodegroup for running worker services
prd_worker_eks_nodegroup = EksNodeGroup(
    name=f"{prd_key}-workers-ng",
    min_size=2,
    max_size=5,
    desired_size=2,
    disk_size=64,
    instance_types=["m5.large"],
    eks_cluster=prd_eks_cluster,
    # Add the workers label to the nodegroup
    labels=workers_ng_label,
    tags=prd_tags,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- ACM certificate for domain
prd_acm_certificate = AcmCertificate(
    name=prd_domain,
    domain_name=prd_domain,
    subject_alternative_names=[f"*.{prd_domain}"],
    store_cert_summary=True,
    certificate_summary_file=ws_dir_path.joinpath("aws", "acm", prd_domain),
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

prd_aws_resources = AwsResourceGroup(
    name=prd_key,
    s3_buckets=[prd_logs_s3_bucket, prd_data_s3_bucket],
    eks_cluster=prd_eks_cluster,
    eks_kubeconfig=prd_eks_kubeconfig,
    eks_nodegroups=[prd_services_eks_nodegroup, prd_worker_eks_nodegroup],
    # Uncomment to create a VPC cloudformation stack
    # cloudformation_stacks=[prd_vpc_stack],
    # Uncomment to create an ACM certificate for domain
    # acm_certificates=[prd_acm_certificate],
)
