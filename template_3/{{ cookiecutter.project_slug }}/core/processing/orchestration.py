# Prefect
from prefect import flow
from prefect.logging import get_run_logger


# Utils
from core.libs.utils import (
    save_artifact,
)

# Tasks
from core.processing.ingestion import task_ingestion
from core.processing.transform import task_transform


@flow(
    name="flow_rockets_launch",
    flow_run_name="flow-rockets-launch",
    log_prints=True,
    description="Flow to orchestrate the ingestion, transformation, and loading of data",
)
def flow_rockets_launch():
    """
    Flow to orchestrate the ingestion, transformation, and loading of data
    """

    # Get logger
    logger = get_run_logger()

    logger.info("-" * 50)
    logger.info("FLOW ROCKETS LAUNCH STARTED")
    logger.info("-" * 50)

    # Run the ingestion flow
    task_ingestion()

    # Run the transformation with dbt
    task_transform()

    # Save the artifact
    save_artifact(key_name="flow-rockets-launch-artifact")

    logger.info("-" * 50)
    logger.info("FLOW ROCKETS LAUNCH COMPLETED")
    logger.info("-" * 50)
