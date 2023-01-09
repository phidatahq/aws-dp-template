from typing import Dict

from phidata.asset.local.file import LocalFile
from phidata.task import TaskArgs, task
from phidata.utils.log import logger

##############################################################################
# A workflow to download crypto price data locally
##############################################################################

# Step 1: Define a File object for storing crypto price data
# Path: `storage/crypto/crypto_prices.csv`
crypto_prices_file = LocalFile(
    name="crypto_prices.csv",
    file_dir="crypto",
)


# Step 2: Create a task that downloads price data
@task
def download_crypto_prices(**kwargs) -> bool:
    import httpx
    import polars as pl

    coins = ["bitcoin", "ethereum"]
    run_date = TaskArgs.from_kwargs(kwargs).run_date

    logger.info(f"Downloading prices for run_date={run_date}")
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
    df = pl.DataFrame(
        [
            {
                "ds": run_date.date(),
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

    # Write the dataframe to file
    return crypto_prices_file.write_df(df)


# Instantiate the task
download_prices = download_crypto_prices()
