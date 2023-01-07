from phidata.app.postgres import PostgresDb

from workflows.env import AIRFLOW_ENV
from workspace.dev.pg_dbs import dev_pg_db, dev_pg_db_connection_id
from workspace.prd.pg_dbs import prd_pg_db, prd_pg_db_connection_id

# -*- Postgres Apps -*-

PG_DB_APP: PostgresDb
if AIRFLOW_ENV == "prd":
    PG_DB_APP = prd_pg_db
else:
    PG_DB_APP = dev_pg_db


# -*- Postgres Connections -*-

PG_DB_CONN_ID: str
if AIRFLOW_ENV == "prd":
    PG_DB_CONN_ID = prd_pg_db_connection_id
else:
    PG_DB_CONN_ID = dev_pg_db_connection_id
