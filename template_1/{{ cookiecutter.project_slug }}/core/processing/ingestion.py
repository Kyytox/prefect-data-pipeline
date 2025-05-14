# Prefect
from prefect import task
from prefect.logging import get_run_logger

# Paths
from core.config.path import PATH

# Utils
from core.libs.utils import upd_data_artifact


@task(
    name="task_ingestion",
    task_run_name="task-ingestion",
    description="Ingest data",
)
def task_ingestion():
    """
    Task to ingest data
    """

    # Get logger
    logger = get_run_logger()

    logger.info("-" * 20)
    logger.info("TASK INGESTION")
    logger.info("-" * 20)

    # Update artifact
    upd_data_artifact(
        info=f"Ingestion data from ...........",
        data=f"xxx rows and xxx columns",
    )
