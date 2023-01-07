from typing import Dict

from phidata.asset.aws.s3.dataset import S3Dataset
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

from workflows.buckets import DATA_S3_BUCKET
from workflows.env import AIRFLOW_ENV

##############################################################################
# A workflow to write hourly cryptocurrency price data to s3
##############################################################################

# List of coins to get prices for
coins = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple",
    "tether",
]

# Step 1: Define dataset for storing crypto price data
crypto_prices_daily_s3 = S3Dataset(
    table=f"crypto_prices_daily_{AIRFLOW_ENV}",
    database="default",
    write_mode="overwrite_partitions",
    partition_cols=["ds"],
    bucket=DATA_S3_BUCKET,
)

# Step 2: Create task to download crypto price data and write to s3 dataset
@task
def load_crypto_prices(**kwargs) -> bool:
    """
    Download crypto price data and write to s3
    """
    import pandas as pd
    import requests

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)
    run_date = args.run_date
    run_day = run_date.strftime("%Y-%m-%d")
    run_hour = run_date.strftime("%H")

    logger.info(f"Downloading prices for: ds={run_day}/hr={run_hour}")
    response: Dict[str, Dict] = requests.get(
        url="https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": ",".join(coins),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true",
        },
    ).json()

    logger.info("Converting response to dataframe")
    _df = pd.DataFrame.from_dict(response, orient="index")
    _df.index.name = "ticker"
    _df["ds"] = run_day
    _df["hr"] = run_hour
    _df["dttm"] = run_date
    _df.reset_index(inplace=True)
    print(_df.head())

    # crypto_prices_daily_s3.delete()
    return crypto_prices_daily_s3.write_pandas_df(_df)


# Step 3: Instantiate the task
download_prices = load_crypto_prices()

# Step 4: Create a Workflow to run these tasks
crypto_prices_daily = Workflow(
    name="crypto_prices_daily_aws",
    tasks=[download_prices],
    # the output of this workflow
    outputs=[crypto_prices_daily_s3],
)
