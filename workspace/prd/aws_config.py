from phidata.infra.aws.config import AwsConfig

from workspace.prd.airflow.aws_resources import prd_airflow_aws_resources
from workspace.prd.aws_resources import prd_aws_resources
from workspace.prd.jupyter.jupyterlab import prd_jupyterlab_aws_resources
from workspace.prd.pg_dbs import prd_pg_db_aws_resources
from workspace.prd.superset.aws_resources import prd_superset_aws_resources
from workspace.settings import prd_env

#
# -*- Define production AWS resources using the AwsConfig
#
prd_aws_config = AwsConfig(
    env=prd_env,
    resources=[
        prd_aws_resources,
        prd_airflow_aws_resources,
        prd_pg_db_aws_resources,
        prd_superset_aws_resources,
        prd_jupyterlab_aws_resources,
    ],
)
