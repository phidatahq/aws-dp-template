from typing import Dict

from phidata.asset.table.s3.parquet import ParquetTable
from phidata.check.df.not_empty import DFNotEmpty
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

from workflows.buckets import DATA_S3_BUCKET

##############################################################################
# A workflow to write cryptocurrency price data to s3
##############################################################################

# Step 1: Define ParquetTable on S3 for storing data
crypto_prices_s3 = ParquetTable(
    name="crypto_prices",
    bucket=DATA_S3_BUCKET,
    partitions=["ds", "hour"],
    write_checks=[DFNotEmpty()],
)


# Step 2: Create task to download crypto price data and write to ParquetTable
@task
def load_crypto_prices(**kwargs) -> bool:
    """
    Download prices and load a ParquetTable on S3.
    """
    import httpx
    import polars as pl

    coins = ["bitcoin", "ethereum", "litecoin", "ripple", "tether"]
    run_date = TaskArgs.from_kwargs(kwargs).run_date
    run_day = run_date.strftime("%Y-%m-%d")
    run_hour = run_date.strftime("%H")

    logger.info(f"Downloading prices for ds={run_day}/hr={run_hour}")
    response: Dict[str, Dict] = httpx.get(
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

    # Create a dataframe from response
    df: pl.DataFrame = pl.DataFrame(
        [
            {
                "ds": run_day,
                "hour": run_hour,
                "ticker": coin_name,
                "usd": coin_data["usd"],
                "usd_market_cap": coin_data["usd_market_cap"],
                "usd_24h_vol": coin_data["usd_24h_vol"],
                "usd_24h_change": coin_data["usd_24h_change"],
                "last_updated_at": coin_data["last_updated_at"],
            }
            for coin_name, coin_data in response.items()
        ]
    )
    logger.info(df.head())

    # Write the dataframe to s3
    return crypto_prices_s3.write_df(df)


# 2.2: Create task to analyze ParquetTable
@task
def analyze_crypto_prices(**kwargs) -> bool:
    """
    Read ParquetTable from S3.
    """
    import polars as pl

    run_date = TaskArgs.from_kwargs(kwargs).run_date
    run_day = run_date.strftime("%Y-%m-%d")
    run_hour = run_date.strftime("%H")

    logger.info(f"Reading prices for ds={run_day}/hr={run_hour}")
    df: pl.DataFrame = crypto_prices_s3.read_df()
    logger.info(df.head())

    return True


# Step 3: Instantiate the tasks
load_prices = load_crypto_prices()
analyze_prices = analyze_crypto_prices()

# Step 4: Create a Workflow to run these tasks
crypto_prices_aws = Workflow(
    name="crypto_prices_aws",
    tasks=[load_prices, analyze_prices],
    # the graph orders analyze_prices to run after load_prices
    graph={
        analyze_prices: [load_prices],
    },
    # the output of this workflow
    outputs=[crypto_prices_s3],
)

# Step 5: Create a DAG to run the workflow on a schedule
dag = crypto_prices_aws.create_airflow_dag(schedule_interval="@hourly")
