from phidata.app.databox import Databox
from phidata.app.group import AppGroup

from workspace.dev.images import dev_databox_image
from workspace.dev.postgres import dev_postgres_airflow_connections
from workspace.settings import ws_settings

#
# -*- Databox Docker resources
#

# -*- Databox
dev_databox = Databox(
    image_name=dev_databox_image.name,
    image_tag=dev_databox_image.tag,
    mount_workspace=True,
    env={
        "AIRFLOW__WEBSERVER__EXPOSE_CONFIG": "True",
        "AIRFLOW__WEBSERVER__EXPOSE_HOSTNAME": "True",
        "AIRFLOW__WEBSERVER__EXPOSE_STACKTRACE": "True",
        # Create aws_default connection_id
        "AWS_DEFAULT_REGION": ws_settings.aws_region,
        "AIRFLOW_CONN_AWS_DEFAULT": "aws://",
        # Airflow Navbar color
        "AIRFLOW__WEBSERVER__NAVBAR_COLOR": "#cffafe",
    },
    env_file=ws_settings.ws_dir.joinpath("env/dev_airflow_env.yml"),
    secrets_file=ws_settings.ws_dir.joinpath("secrets/dev_airflow_secrets.yml"),
    use_cache=ws_settings.use_cache,
    db_connections=dev_postgres_airflow_connections,
    # Access the databox airflow webserver on http://localhost:8390
    airflow_standalone_host_port=8390,
    # Mark as false after first run
    # Init airflow db on container start -- mark as false after first run
    init_airflow_db=True,
    # Upgrade the airflow db on container start -- mark as false after first run
    upgrade_airflow_db=True,
    # Creates airflow user: admin, pass: admin -- mark as false after first run
    create_airflow_admin_user=True,
    # Run the airflow webserver on airflow.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.databox.entrypoints": "http",
        "traefik.http.routers.databox.rule": "Host(`databox.dp`)",
        # point the traefik loadbalancer to the webserver_port on the container
        "traefik.http.services.databox.loadbalancer.server.port": "8080",
    },
)

dev_databox_apps = AppGroup(
    name="databox",
    enabled=ws_settings.dev_databox_enabled,
    apps=[dev_databox],
)
