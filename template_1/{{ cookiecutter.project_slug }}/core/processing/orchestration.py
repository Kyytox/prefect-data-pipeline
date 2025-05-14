# Prefect
from prefect import flow
from prefect.logging import get_run_logger

# Utils
from core.libs.utils import save_artifact

# Tasks
from core.processing.ingestion import task_ingestion
from core.processing.transform import task_transform


@flow(
    name="my_test_flow",
    flow_run_name="my-test-flow",
    log_prints=True,
    description="Flow to orchestrate the ingestion, transformation, and loading of data",
)
def my_test_flow():
    """
    Flow to orchestrate the ingestion, transformation, and loading of data
    """

    # Get logger
    logger = get_run_logger()

    logger.info("-" * 50)
    logger.info("FLOW TEST START")
    logger.info("-" * 50)

    # Run the ingestion flow
    task_ingestion()

    # Run the transformation flow
    task_transform()

    # Save the artifact
    save_artifact(key_name="my_test_flow")

    logger.info("-" * 50)
    logger.info("FLOW TEST END")
    logger.info("-" * 50)
