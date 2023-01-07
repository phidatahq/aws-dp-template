from phidata.app.group import AppGroup
from phidata.app.postgres import PostgresDb

from workspace.settings import pg_dbs_enabled, ws_name

# -*- Dev databases on docker

# Dev pg-db: A postgres instance to use for dev data
dev_pg_db = PostgresDb(
    name=f"dev-pg-{ws_name}",
    db_user=ws_name,
    db_password=ws_name,
    db_schema=ws_name,
    # Connect to this db on port 8315
    container_host_port=8315,
)
dev_pg_db_connection_id = "pg_db"

dev_pg_db_airflow_connections = {
    dev_pg_db_connection_id: dev_pg_db.get_db_connection_url_docker()
}

dev_pg_db_apps = AppGroup(
    name="pg-db",
    enabled=False,
    apps=[dev_pg_db],
)
