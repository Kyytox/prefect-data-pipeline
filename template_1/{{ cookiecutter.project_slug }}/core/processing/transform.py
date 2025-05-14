import pandas as pd

# Prefect
from prefect import task
from prefect.logging import get_run_logger

# Paths
from core.config.path import PATH

# Utils
from core.libs.utils import upd_data_artifact


@task(
    name="task_transform",
    task_run_name="task-transform",
    description="Transform data from data/raw",
)
def task_transform():
    """
    Task to transform data
    """

    # Get logger
    logger = get_run_logger()

    logger.info("-" * 20)
    logger.info("TASK TRANSFORMATION")
    logger.info("-" * 20)

    # Update artifact
    upd_data_artifact(
        info=f"Transformation data from ............",
        data=f"xxx rows and xxx columns",
    )
