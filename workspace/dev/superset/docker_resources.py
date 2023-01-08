from pathlib import Path

from phidata.app.group import AppGroup
from phidata.app.postgres import PostgresDb
from phidata.app.redis import Redis
from phidata.app.superset import SupersetInit, SupersetWebserver

from workspace.dev.images import dev_superset_image
from workspace.settings import ws_settings

#
# -*- Superset Docker resources
#

# Superset db: A postgres instance to use as the database for superset
dev_superset_db = PostgresDb(
    name=f"superset-db-{ws_settings.ws_name}",
    db_user="superset",
    db_password="superset",
    db_schema="superset",
    # Connect to this db on port 8340
    container_host_port=8340,
)

# Superset redis: A redis instance to use as the celery backend for superset
dev_superset_redis = Redis(
    name=f"superset-redis-{ws_settings.ws_name}",
    command=["redis-server", "--save", "60", "1", "--loglevel", "debug"],
    container_host_port=8341,
)

# -*- Settings
# waits for superset-db to be ready before starting app
wait_for_db: bool = True
# waits for superset-redis to be ready before starting app
wait_for_redis: bool = True
# Mount the resources dir using a docker volume
mount_resources: bool = True
dev_superset_resources: str = "workspace/dev/superset/resources"
# Read env variables from env/dev_superset_env.yml
dev_superset_env_file: Path = ws_settings.ws_dir.joinpath(
    "env/dev_superset_env.yml"
)
# Read secrets from secrets/dev_superset_secrets.yml
dev_superset_secrets_file: Path = ws_settings.ws_dir.joinpath(
    "secrets/dev_superset_secrets.yml"
)

# Superset webserver
dev_superset_ws = SupersetWebserver(
    image_name=dev_superset_image.name,
    image_tag=dev_superset_image.tag,
    db_app=dev_superset_db,
    wait_for_db=wait_for_db,
    redis_app=dev_superset_redis,
    wait_for_redis=wait_for_redis,
    mount_resources=mount_resources,
    resources_dir=dev_superset_resources,
    env_file=dev_superset_env_file,
    secrets_file=dev_superset_secrets_file,
    use_cache=ws_settings.use_cache,
    # Access the superset webserver on http://localhost:8410
    app_host_port=8410,
    # Run the superset webserver on superset.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.superset-ws.entrypoints": "http",
        "traefik.http.routers.superset-ws.rule": "Host(`superset.dp`)",
        # point the traefik loadbalancer to the app_port on the container
        "traefik.http.services.superset-ws.loadbalancer.server.port": "8088",
    },
)

# Superset init
superset_init_enabled = True  # Mark as False after first run
dev_superset_init = SupersetInit(
    enabled=superset_init_enabled,
    image_name=dev_superset_image.name,
    image_tag=dev_superset_image.tag,
    db_app=dev_superset_db,
    wait_for_db=wait_for_db,
    redis_app=dev_superset_redis,
    wait_for_redis=wait_for_redis,
    mount_resources=mount_resources,
    resources_dir=dev_superset_resources,
    env_file=dev_superset_env_file,
    secrets_file=dev_superset_secrets_file,
    use_cache=ws_settings.use_cache,
    load_examples=False,
)

dev_superset_apps = AppGroup(
    name="superset",
    enabled=ws_settings.dev_superset_enabled,
    apps=[
        dev_superset_db,
        dev_superset_redis,
        dev_superset_ws,
        dev_superset_init,
    ],
)
