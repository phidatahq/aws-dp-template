from phidata.app.group import AppGroup
from phidata.app.postgres import PostgresDb, PostgresVolumeType
from phidata.infra.aws.resource.group import AwsResourceGroup, EbsVolume

from workspace.prd.aws_resources import services_ng_label
from workspace.settings import (
    aws_az_1a,
    pg_dbs_enabled,
    prd_key,
    prd_tags,
    ws_dir_path,
    ws_name,
)

# -*- Settings
# Prevents deletion of aws resources when running `phi ws down`
aws_skip_delete: bool = False

#
# -*- AWS resources
#
# -*- EbsVolumes
# EbsVolume for pg-db
prd_pg_db_volume = EbsVolume(
    name=f"pg-db-{prd_key}",
    size=32,
    availability_zone=aws_az_1a,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

prd_pg_db_aws_resources = AwsResourceGroup(
    name="pg-db",
    enabled=pg_dbs_enabled,
    volumes=[prd_pg_db_volume],
)

#
# -*- Kubernetes resources
#
# pg-db: A postgres instance to use for stg data
prd_pg_db = PostgresDb(
    name=f"pg-db-{ws_name}",
    volume_type=PostgresVolumeType.AWS_EBS,
    ebs_volume=prd_pg_db_volume,
    secrets_file=ws_dir_path.joinpath("secrets/prd_pg_db_secrets.yml"),
    pod_node_selector=services_ng_label,
)
prd_pg_db_connection_id = "pg_db"

prd_db_airflow_connections = {
    prd_pg_db_connection_id: prd_pg_db.get_db_connection_url_k8s()
}

prd_pg_db_apps = AppGroup(
    name="pg-db",
    enabled=pg_dbs_enabled,
    apps=[prd_pg_db],
)
