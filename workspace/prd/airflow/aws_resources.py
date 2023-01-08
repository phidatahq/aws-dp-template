from phidata.infra.aws.resource.group import (
    AwsResourceGroup,
    CacheCluster,
    CacheSubnetGroup,
    DbInstance,
    DbSubnetGroup,
    EbsVolume,
)

from workspace.prd.aws_resources import prd_vpc_stack
from workspace.settings import (
    airflow_enabled,
    aws_az_1a,
    prd_key,
    prd_tags,
    subnet_ids,
    security_groups,
    ws_dir_path,
)

#
# -*- AWS resources
#

# -*- Settings
# Use RDS as database instead of running postgres on k8s
use_rds: bool = False
# Use ElastiCache as cache instead of running redis on k8s
use_elasticache: bool = False
# Do not create the resource when running `phi ws up`
skip_create: bool = False
# Do not delete the resource when running `phi ws down`
skip_delete: bool = False
# Wait for the resource to be created
wait_for_create: bool = True
# Wait for the resource to be deleted
wait_for_delete: bool = False

# -*- EbsVolumes for airflow database and cache
# NOTE: For production, use RDS and ElastiCache instead of running postgres/redis on k8s.
# EbsVolume for airflow-db
prd_airflow_db_volume = EbsVolume(
    name=f"airflow-db-{prd_key}",
    enabled=(not use_rds),
    size=32,
    tags=prd_tags,
    availability_zone=aws_az_1a,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)
# EbsVolume for airflow-redis
prd_airflow_redis_volume = EbsVolume(
    name=f"airflow-redis-{prd_key}",
    enabled=(not use_elasticache),
    size=16,
    tags=prd_tags,
    availability_zone=aws_az_1a,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- RDS Database Subnet Group
prd_rds_subnet_group = DbSubnetGroup(
    name=f"{prd_key}-db-sg",
    enabled=use_rds,
    # subnet_ids=subnet_ids,
    vpc_stack=prd_vpc_stack,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- Elasticache Subnet Group
prd_elasticache_subnet_group = CacheSubnetGroup(
    name=f"{prd_key}-cache-sg",
    enabled=use_elasticache,
    # subnet_ids=subnet_ids,
    vpc_stack=prd_vpc_stack,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- RDS Database Instance
db_engine = "postgres"
prd_airflow_rds_db = DbInstance(
    name=f"airflow-db-{prd_key}",
    enabled=use_rds,
    engine=db_engine,
    engine_version="14.5",
    allocated_storage=100,
    # NOTE: For production, use a larger instance type.
    # Last checked price: $0.152 per hour = ~$110 per month
    db_instance_class="db.m6g.large",
    availability_zone=aws_az_1a,
    db_subnet_group=prd_rds_subnet_group,
    enable_performance_insights=True,
    vpc_security_group_ids=security_groups,
    secrets_file=ws_dir_path.joinpath("secrets/prd_airflow_db_secrets.yml"),
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- Elasticache Redis Cluster
prd_airflow_redis_cluster = CacheCluster(
    name=f"airflow-cache-{prd_key}",
    enabled=use_elasticache,
    engine="redis",
    num_cache_nodes=1,
    # NOTE: For production, use a larger instance type.
    # Last checked price: $0.068 per hour = ~$50 per month
    cache_node_type="cache.t2.medium",
    security_group_ids=security_groups,
    cache_subnet_group=prd_elasticache_subnet_group,
    preferred_availability_zone=aws_az_1a,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

prd_airflow_aws_resources = AwsResourceGroup(
    name="airflow",
    enabled=airflow_enabled,
    db_instances=[prd_airflow_rds_db],
    db_subnet_groups=[prd_rds_subnet_group],
    cache_clusters=[prd_airflow_redis_cluster],
    cache_subnet_groups=[prd_elasticache_subnet_group],
    volumes=[prd_airflow_db_volume, prd_airflow_redis_volume],
)
