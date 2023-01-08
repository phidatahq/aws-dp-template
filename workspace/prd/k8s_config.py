from phidata.infra.k8s.config import K8sConfig

from workspace.k8s.whoami import whoami_k8s_rg
from workspace.prd.airflow.k8s_apps import prd_airflow_apps
from workspace.prd.aws_resources import prd_eks_cluster
from workspace.prd.jupyter.jupyterlab import prd_jupyterlab_apps
from workspace.prd.pg_dbs import prd_pg_db_apps
from workspace.prd.superset.k8s_apps import prd_superset_apps
from workspace.prd.traefik import prd_traefik_apps
from workspace.settings import prd_env

#
# -*- Define production Kubernetes resources using the K8sConfig
#
prd_k8s_config = K8sConfig(
    env=prd_env,
    app_groups=[
        prd_airflow_apps,
        prd_superset_apps,
        prd_pg_db_apps,
        prd_traefik_apps,
        prd_jupyterlab_apps,
    ],
    create_resources=[whoami_k8s_rg],
    eks_cluster=prd_eks_cluster,
)
