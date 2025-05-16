import os
from dotenv import load_dotenv

# Prefect
from prefect import task
from prefect.logging import get_run_logger
from prefect_dbt.cli.commands import DbtCoreOperation

# Paths
from core.config.path import PATH_CONFIG_SCHEMA

# Utils
from core.libs.utils import upd_data_artifact

load_dotenv()


@task(
    name="task_transform",
    task_run_name="task-transform",
    description="Transform data using DBT",
)
def task_transform():
    """
    Task to transform data using DBT

    This task runs DBT models to transform data in PostgreSQL
    """
    logger = get_run_logger()

    # Load environment variables from .env file
    os.environ["DB_USER"] = os.getenv("DB_USER")
    os.environ["DBT_ENV_SECRET_DB_PASSWORD"] = os.getenv("DBT_ENV_SECRET_DB_PASSWORD")
    os.environ["DB_NAME"] = os.getenv("DB_NAME")

    # Run DBT models to transform data
    try:
        DbtCoreOperation(
            commands=["dbt run"],
            project_dir="dbt_project",
            profiles_dir="dbt_project",
        ).run()

        upd_data_artifact(
            info=f"Country launch statistics", data="Transformation completed"
        )
    except Exception as e:
        logger.error(f"Error running DBT: {e}")
