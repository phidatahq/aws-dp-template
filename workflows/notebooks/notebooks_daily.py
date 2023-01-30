from pathlib import Path

from airflow.models import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.utils.dates import days_ago

DAG_ID = "notebooks_daily"
EMAILS = ["alerts@datateam.com"]

default_task_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "start_date": days_ago(1),
    "email": EMAILS,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
}

workflows_dir = Path(__file__).parent.parent
notebooks_dir = workflows_dir.parent.joinpath("notebooks")

with DAG(
    dag_id=DAG_ID,
    description="Run notebooks daily",
    default_args=default_task_args,
    tags=["notebooks"],
    catchup=False,
) as dag:

    crypto_nb = PapermillOperator(
        task_id="crypto_nb",
        input_nb=str(notebooks_dir.joinpath("examples", "crypto_nb.ipynb")),
        # The output notebook will be saved to the outputs directory
        # The outputs directory is ignored from git
        output_nb=str(notebooks_dir.joinpath("outputs", "crypto_nb_{{ execution_date }}.ipynb")),
        parameters={"run_date": "{{ execution_date }}"},
    )
