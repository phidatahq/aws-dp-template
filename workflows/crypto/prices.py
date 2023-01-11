from typing import Dict

from phidata.asset.table.local.csv import CsvTable
from phidata.check.df.not_empty import DFNotEmpty
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

##############################################################################
# A workflow to download crypto price data locally
##############################################################################

# Step 1: Define CsvTable for storing data
# Path: `storage/tables/crypto_prices`
crypto_prices_local = CsvTable(
    name="crypto_prices",
    database="crypto",
    partitions=["ds"],
    write_checks=[DFNotEmpty()],
)


# Step 2: Create task to download crypto price data and write to CsvTable
@task
def load_crypto_prices(**kwargs) -> bool:
    """
    Download prices and load a CsvTable.
    """
    import httpx
    import polars as pl

    coins = ["bitcoin", "ethereum"]
    run_date = TaskArgs.from_kwargs(kwargs).run_date
    run_day = run_date.strftime("%Y-%m-%d")

    logger.info(f"Downloading prices for ds={run_day}")
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

    # Create a dataframe from the response
    df: pl.DataFrame = pl.DataFrame(
        [
            {
                "ds": run_day,
                "ticker": coin_name,
                "usd:": coin_data["usd"],
                "usd_market_cap": coin_data["usd_market_cap"],
                "usd_24h_vol": coin_data["usd_24h_vol"],
                "usd_24h_change": coin_data["usd_24h_change"],
                "last_updated_at": coin_data["last_updated_at"],
            }
            for coin_name, coin_data in response.items()
        ]
    )
    logger.info(df.head())

    # Write the dataframe locally
    return crypto_prices_local.write_df(df)


# 2.2: Create a task to analyze CsvTable
@task
def analyze_crypto_prices(**kwargs) -> bool:
    """
    Read CsvTable
    """
    import polars as pl
    import pyarrow.dataset as ds

    run_date = TaskArgs.from_kwargs(kwargs).run_date
    run_day = run_date.strftime("%Y-%m-%d")

    logger.info(f"Reading prices for ds={run_day}")
    df: pl.DataFrame = crypto_prices_local.read_df(filter=(ds.field("ds") == run_day))
    logger.info(df.head())

    return True


# Step 3: Instantiate the tasks
load_prices = load_crypto_prices()
analyze_prices = analyze_crypto_prices()

# Step 4: Create a Workflow to run these tasks
crypto_prices_aws = Workflow(
    name="crypto_prices",
    tasks=[load_prices, analyze_prices],
    outputs=[crypto_prices_local],
)
