from phidata.asset.aws.s3.csv_dataset import S3DatasetCsv
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

from workflows.buckets import DATA_S3_BUCKET
from workflows.env import AIRFLOW_ENV

##############################################################################
# As workflow for calculating daily active users using s3 and athena
##############################################################################

# Step 1: Define datasets for storing user activity and daily active users
user_activity_s3 = S3DatasetCsv(
    table=f"user_activity_{AIRFLOW_ENV}",
    database="default",
    write_mode="overwrite_partitions",
    partition_cols=["ds"],
    bucket=DATA_S3_BUCKET,
)
daily_active_users_s3 = S3DatasetCsv(
    table=f"daily_active_users_{AIRFLOW_ENV}",
    database="default",
    write_mode="overwrite_partitions",
    partition_cols=["ds"],
    bucket=DATA_S3_BUCKET,
)

# Step 2: Create task to download user activity data and write to s3 dataset
@task
def load_user_activity(**kwargs) -> bool:
    """
    Download user activity data and write to s3
    """
    import pandas as pd

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)

    run_ds = args.run_date.strftime("%Y-%m-%d")
    logger.info(f"Downloading user activity for: ds={run_ds}")
    _df = pd.read_csv(
        "https://raw.githubusercontent.com/phidatahq/demo-data/main/dau_2021_10_01.csv"
    )
    _df.reset_index(drop=True, inplace=True)
    print(_df.head())

    return user_activity_s3.write_pandas_df(_df)


# Step 3: Create task to calculate daily active users and write to s3 dataset
@task
def load_daily_active_users(**kwargs) -> bool:
    """
    Calculate daily active users and write to s3
    """

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)

    run_ds = args.run_date.strftime("%Y-%m-%d")
    logger.info(f"Calculating daily active users for: ds={run_ds}")
    return daily_active_users_s3.create_from_query(
        sql=f"""
            SELECT
                SUM(CASE WHEN is_active=1 THEN 1 ELSE 0 END) AS active_users,
                ds
            FROM {user_activity_s3.name}
            GROUP BY ds
            """,
        wait=True,
        drop_before_create=True,
    )


# Step 4: Instantiate the tasks
download_user_activity = load_user_activity()
load_dau = load_daily_active_users()

# Step 5: Create a Workflow to run tasks
dau_aws = Workflow(
    name="dau_aws",
    tasks=[download_user_activity, load_dau],
    # the graph orders load_dau to run after download_user_activity
    graph={load_dau: [download_user_activity]},
    # the outputs of this workflow
    outputs=[user_activity_s3, daily_active_users_s3],
)
