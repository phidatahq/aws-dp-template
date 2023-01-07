from phidata.infra.docker.config import DockerConfig

from workspace.dev.airflow.docker_resources import dev_airflow_apps
from workspace.dev.images import dev_images
from workspace.dev.jupyter.docker_resources import dev_jupyter_apps
from workspace.dev.pg_dbs import dev_pg_db_apps
from workspace.dev.superset.docker_resources import dev_superset_apps
from workspace.dev.traefik import dev_traefik_resources
from workspace.settings import dev_env, ws_name

#
# -*- Define dev Docker resources using the DockerConfig
#
dev_docker_config = DockerConfig(
    env=dev_env,
    network=ws_name,
    app_groups=[dev_pg_db_apps, dev_airflow_apps, dev_jupyter_apps, dev_superset_apps],
    # uncomment the following line to build local images
    images=dev_images,
    resources=[dev_traefik_resources],
)
