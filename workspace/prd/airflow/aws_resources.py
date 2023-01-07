from phidata.infra.aws.resource.group import (
    AwsResourceGroup,
    CacheCluster,
    CacheSubnetGroup,
    DbInstance,
    DbSubnetGroup,
    EbsVolume,
)

from workspace.settings import (
    airflow_enabled,
    aws_az_1a,
    prd_key,
    prd_tags,
    private_subnets,
    security_groups,
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
# Use RDS as database instead of running postgres on k8s
use_rds: bool = True
# Use ElastiCache as cache instead of running redis on k8s
use_elasticache: bool = True

# -*- EbsVolumes for airflow database and cache
# NOTE: For production, use RDS and ElastiCache instead of running postgres/redis on k8s.
# EbsVolume for airflow-db
prd_airflow_db_volume = EbsVolume(
    name=f"airflow-db-{prd_key}",
    enabled=(not use_rds),
    size=32,
    availability_zone=aws_az_1a,
    tags=prd_tags,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)
# EbsVolume for airflow-redis
prd_airflow_redis_volume = EbsVolume(
    name=f"airflow-redis-{prd_key}",
    enabled=(not use_elasticache),
    size=16,
    availability_zone=aws_az_1a,
    tags=prd_tags,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- RDS Database Subnet Group
prd_rds_subnet_group = DbSubnetGroup(
    name=f"{prd_key}-db-sg",
    enabled=use_rds,
    subnet_ids=private_subnets,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

# -*- Elasticache Subnet Group
prd_elasticache_subnet_group = CacheSubnetGroup(
    name=f"{prd_key}-cache-sg",
    enabled=use_elasticache,
    subnet_ids=private_subnets,
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
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
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
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
    skip_create=aws_skip_create,
    skip_delete=aws_skip_delete,
    wait_for_creation=aws_wait_for_create,
    wait_for_deletion=aws_wait_for_delete
)

prd_airflow_aws_resources = AwsResourceGroup(
    name="airflow",
    enabled=airflow_enabled,
    volumes=[prd_airflow_db_volume, prd_airflow_redis_volume],
    db_instances=[prd_airflow_rds_db],
    db_subnet_groups=[prd_rds_subnet_group],
    cache_clusters=[prd_airflow_redis_cluster],
    cache_subnet_groups=[prd_elasticache_subnet_group],
)
