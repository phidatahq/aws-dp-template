from typing import Dict

from phidata.asset.table.sql.postgres import PostgresTable
from phidata.task import TaskArgs, task
from phidata.utils.log import logger
from phidata.workflow import Workflow

from workflows.sql_dbs import POSTGRES_APP, POSTGRES_CONN_ID

##############################################################################
# A workflow to loads daily cryptocurrency price data to a
# postgres table: `crypto_prices_daily`
##############################################################################

# Step 1: Define a postgres table for storing crypto price data
crypto_prices_daily_pg = PostgresTable(
    name="crypto_prices_daily",
    # use the connection URL from the dev_pg_db object
    db_app=POSTGRES_APP,
    # provide the connection ID used by airflow
    airflow_conn_id=POSTGRES_CONN_ID,
)


# Step 2: Create tasks to load the crypto_prices_daily table
# 2.1 Download price data
@task
def load_crypto_prices(**kwargs) -> bool:
    """
    Download prices and load postgres table.
    """
    import httpx
    import polars as pl

    coins = ["bitcoin", "ethereum", "litecoin", "ripple", "tether"]
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
                "hour": run_date.strftime("%H"),
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

    # Write the dataframe to table
    return crypto_prices_daily_pg.write_df(df, if_exists="append")


# 2.2 Drop existing price data to prevent duplicates
@task
def drop_existing_prices(**kwargs) -> bool:
    """
    Drop rows for current window (ds + hour) to prevent duplicates
    """
    args: TaskArgs = TaskArgs.from_kwargs(kwargs)
    run_date = args.run_date
    run_day = run_date.strftime("%Y-%m-%d")
    run_hour = run_date.strftime("%H")

    logger.info(f"Dropping rows for: ds={run_day}/hr={run_hour}")
    try:
        crypto_prices_daily_pg.run_sql_query(
            f"""
            DELETE FROM {crypto_prices_daily_pg.name}
            WHERE
                ds = '{run_day}'
            """
        )
    except Exception as e:
        logger.error(f"Error dropping rows: {e}")
    return True


# Step 3: Instantiate the tasks
download_prices = load_crypto_prices()
drop_prices = drop_existing_prices(enabled=False)

# Step 4: Create a Workflow to run these tasks
crypto_prices = Workflow(
    name="crypto_prices",
    tasks=[drop_prices, download_prices],
    # the graph orders download_prices to run after drop_prices
    graph={
        download_prices: [drop_prices],
    },
    # the output of this workflow
    outputs=[crypto_prices_daily_pg],
)

# Step 5: Create a DAG to run the workflow on a schedule
dag = crypto_prices.create_airflow_dag(
    schedule_interval="@daily",
    is_paused_upon_creation=True,
)
