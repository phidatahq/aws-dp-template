from typing import Dict

from phidata.asset.file import File
from phidata.task import TaskArgs, task
from phidata.utils.log import logger

##############################################################################
# A workflow to download crypto price data locally
##############################################################################

# Step 1: Define a File object for storing crypto price data
# Path: `storage/crypto/crypto_prices.csv`
crypto_prices_file = File(
    name="crypto_prices.csv",
    file_dir="crypto",
)

# Step 2: Create a task that downloads price data
@task
def download_crypto_prices(**kwargs) -> bool:
    import pandas as pd
    import requests

    coins = ["bitcoin", "ethereum"]
    run_date = TaskArgs.from_kwargs(kwargs).run_date

    logger.info(f"Downloading prices for run_date={run_date}")
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
    _df["dttm"] = run_date
    _df.reset_index(inplace=True)
    _df.set_index(["dttm", "ticker"], inplace=True)

    print(_df.head())

    return crypto_prices_file.write_pandas_df(_df)


# Instantiate the task
download_prices = download_crypto_prices()
