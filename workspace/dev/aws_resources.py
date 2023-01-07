from phidata.infra.aws.config import AwsResourceGroup
from phidata.infra.aws.resource.s3.bucket import S3Bucket

from workspace.settings import dev_key

#
# -*- AWS resources
#

# -*- Settings
# Prevents deletion when running `phi ws down`
aws_skip_delete: bool = False

# -*- S3 buckets
# S3 bucket for storing logs
dev_logs_s3_bucket = S3Bucket(
    name=f"{dev_key}-logs",
    skip_delete=aws_skip_delete,
)

# S3 bucket for storing data
dev_data_s3_bucket = S3Bucket(
    name=f"{dev_key}-data",
    skip_delete=aws_skip_delete,
)

dev_aws_resources = AwsResourceGroup(
    name=dev_key,
    s3_buckets=[dev_logs_s3_bucket, dev_data_s3_bucket],
)
