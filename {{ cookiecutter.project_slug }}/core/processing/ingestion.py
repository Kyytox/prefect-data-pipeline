from prefect import flow, task
from prefect.logging import get_run_logger

from prefect.states import Completed

# Paths
from core.config.path import PATH_DATA_SOURCE, PATH_DATA_RAW

# Utils
from core.libs.utils import (
    load_csv,
    save_parquet,
    upd_data_artifact,
    save_artifact,
)


@flow(
    name="flow_ingestion",
    flow_run_name="flow-ingestion",
    log_prints=True,
    description="Ingest data from data/sources",
)
def flow_ingestion():
    """
    Flow to ingest data from data/sources
    """

    # Get logger
    logger = get_run_logger()

    file_src = f"{PATH_DATA_SOURCE}/github_repo.csv"
    file_dest = f"{PATH_DATA_RAW}/github_repo.parquet"

    # Load data
    df = load_csv(
        file_path=file_src,
        sep=",",
        encoding="utf-8",
        header=0,
    )

    # display infos
    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"DataFrame columns: {df.info()}")
    logger.info(f"DataFrame head: {df.head()}")

    # Update artifact
    upd_data_artifact(
        info=f"Ingestion data from {file_src}",
        data=f"{df.shape[0]} rows and {df.shape[1]} columns",
    )

    # Save data
    save_parquet(
        df=df,
        file_path=file_dest,
        index=False,
    )

    # Save artifact
    save_artifact(key_name="flow-ingestion-artifact")

    # Return the flow state
    return Completed(message="Flow ingestion completed successfully")
