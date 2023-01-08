from phidata.app.group import AppGroup
from phidata.app.postgres import PostgresDb

from workspace.settings import ws_settings

# -*- Run a postgres database on docker

# Dev pg-db: A postgres instance to use for dev data
dev_pg_db = PostgresDb(
    name=f"dev-pg-{ws_settings.ws_name}",
    db_user=ws_settings.ws_name,
    db_password=ws_settings.ws_name,
    db_schema=ws_settings.ws_name,
    # Connect to this db on port 8315
    container_host_port=8315,
)

dev_pg_db_connection_id = "dev_pg"
dev_pg_db_airflow_connections = {
    dev_pg_db_connection_id: dev_pg_db.get_db_connection_url_docker()
}

dev_postgres_apps = AppGroup(
    name="postgres",
    enabled=ws_settings.dev_postgres_enabled,
    apps=[dev_pg_db],
)
