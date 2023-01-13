from phidata.docker.config import DockerConfig

from workspace.dev.airflow.docker_resources import dev_airflow_apps
from workspace.dev.assistant import dev_assistant
from workspace.dev.databox.docker_resources import dev_databox_apps
from workspace.dev.images import dev_images
from workspace.dev.jupyter.docker_resources import dev_jupyter_apps
from workspace.dev.postgres import dev_postgres_apps
from workspace.dev.superset.docker_resources import dev_superset_apps
from workspace.dev.traefik import dev_traefik_resources
from workspace.settings import ws_settings

#
# -*- Define dev Docker resources using the DockerConfig
#
dev_docker_config = DockerConfig(
    env=ws_settings.dev_env,
    network=ws_settings.ws_name,
    apps=[dev_assistant],
    app_groups=[
        dev_postgres_apps,
        dev_airflow_apps,
        dev_databox_apps,
        dev_jupyter_apps,
        dev_superset_apps,
    ],
    images=dev_images,
    resources=[dev_traefik_resources],
)
