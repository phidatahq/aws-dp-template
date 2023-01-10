from typing import Dict

from phidata.asset.table.s3.parquet import ParquetTable
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

from workflows.buckets import DATA_S3_BUCKET

##############################################################################
# A workflow to write cryptocurrency price data to s3
##############################################################################

# Step 1: Define ParquetTable on S3 for storing data
crypto_prices_daily_s3 = ParquetTable(
    name="crypto_prices_daily",
    bucket=DATA_S3_BUCKET,
    partitions=["ds", "hour"],
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
    df = pl.DataFrame(
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
    return crypto_prices_daily_s3.write_df(df)


# Step 3: Instantiate the task
download_prices = load_crypto_prices()

# Step 4: Create a Workflow to run these tasks
crypto_prices_daily = Workflow(
    name="crypto_prices_daily_aws",
    tasks=[download_prices],
    # the output of this workflow
    outputs=[crypto_prices_daily_s3],
)
