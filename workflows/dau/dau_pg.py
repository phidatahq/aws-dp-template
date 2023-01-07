from phidata.asset.table.sql.postgres import PostgresTable
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

from workflows.sql_dbs import PG_DB_APP, PG_DB_CONN_ID

##############################################################################
# A workflow for calculating daily active users using postgres
##############################################################################

# Step 1: Define tables for storing user activity and daily active users
user_activity_pg = PostgresTable(
    name="user_activity",
    db_app=PG_DB_APP,
    airflow_conn_id=PG_DB_CONN_ID,
)
daily_active_users_pg = PostgresTable(
    name="daily_active_users",
    db_app=PG_DB_APP,
    airflow_conn_id=PG_DB_CONN_ID,
)

# Step 2: Create task to download user activity data and write to postgres table
@task
def load_user_activity(**kwargs) -> bool:
    """
    Download user activity data and write to postgres table
    """
    import pandas as pd

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)

    run_ds = args.run_date.strftime("%Y-%m-%d")
    logger.info(f"Downloading user activity for: ds={run_ds}")
    _df = pd.read_csv(
        "https://raw.githubusercontent.com/phidatahq/demo-data/main/dau_2021_10_01.csv"
    )
    _df.reset_index(drop=True, inplace=True)
    _df.set_index("ds", inplace=True)
    print(_df.head())

    return user_activity_pg.write_pandas_df(_df, if_exists="replace")


# Step 3: Create task to calculate daily active users and write to postgres table
@task
def load_daily_active_users(**kwargs) -> bool:
    """
    Calculate daily active users and write to postgres table
    """
    import pandas as pd

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)

    run_ds = args.run_date.strftime("%Y-%m-%d")
    logger.info(f"Calculating daily active users for: ds={run_ds}")
    _df = pd.read_sql(
        f"""
        SELECT
            ds,
            SUM(CASE WHEN is_active=1 THEN 1 ELSE 0 END) AS active_users
        FROM {user_activity_pg.name}
        GROUP BY ds
        """,
        con=user_activity_pg.create_db_engine(),
    )
    _df.reset_index(drop=True, inplace=True)
    _df.set_index("ds", inplace=True)
    print(_df.head())

    return daily_active_users_pg.write_pandas_df(_df, if_exists="replace")


# Step 4: Instantiate the tasks
download_user_activity = load_user_activity()
load_dau = load_daily_active_users()

# Step 5: Create a Workflow to run these tasks
dau = Workflow(
    name="dau",
    tasks=[download_user_activity, load_dau],
    # the graph orders load_dau to run after download_user_activity
    graph={load_dau: [download_user_activity]},
    # the outputs of this workflow
    outputs=[user_activity_pg, daily_active_users_pg],
)

# Step 6: Create a DAG to run the workflow on a schedule
# dag = dau.create_airflow_dag(
#     is_paused_upon_creation=True,
# )
