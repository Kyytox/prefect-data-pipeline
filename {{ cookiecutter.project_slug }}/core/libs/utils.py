from pathlib import Path
import pandas as pd

from prefect import task
from prefect.logging import get_run_logger
from prefect.variables import Variable
from prefect.artifacts import create_table_artifact


def upd_data_artifact(info, data):
    """
    Update Artifact

    - Retrieve the artifact from the Prefect Variable
    - Add data to the artifact
        - Save the artifact back to the Prefect Variable

    Args:
        info: information
        data: data to add
    """

    # get varoaible
    data_artifact = Variable.get("data_artifact", default=[])

    # add data
    data_artifact.append({"info": info, "data": data})

    # save variable
    Variable.set("data_artifact", data_artifact, overwrite=True)


def save_artifact(key_name: str):
    """
    Save artifact in Prefect for the Flow

    - Retrieve the artifact from the Prefect Variable
    - save the artifact with the data
    - Reset the Prefect Variable for the next run

    Args:
        key: key of artifact (name of the artifact)
    """

    # get data
    data_artifact = Variable.get("data_artifact", default=[])

    # create data
    create_table_artifact(
        key=key_name,
        table=data_artifact,
    )

    # reset variable
    Variable.set("data_artifact", [], overwrite=True)


@task(
    name="load_csv",
    description="Load CSV file",
    task_run_name="load-csv-{file_path}",
)
def load_csv(file_path: str, **kwargs) -> pd.DataFrame:
    """
        Load data from a CSV file.

    Args:
        File_path: path to the CSV file

    Returns:
        Pandas Dataframe containing CSV data
    """
    # Get logger
    logger = get_run_logger()

    logger.info(f"Loading data from {file_path}")

    try:
        # Read the CSV file
        df = pd.read_csv(file_path, **kwargs)

        logger.info(f"Load Success: {len(df)} rows, {df.columns.size} columns")

        return df
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        raise


@task(
    name="save_parquet",
    description="Save DataFrame to Parquet file",
    task_run_name="save-parquet-{file_path}",
)
def save_parquet(df: pd.DataFrame, file_path: str, **kwargs) -> str:
    """
    Save a DataFrame to a Parquet file.

    Args:
        df: DataFrame to save
        file_path: Path to save the Parquet file
    """
    # Get logger
    logger = get_run_logger()

    if df.empty:
        logger.warning(f"DataFrame is empty, nothing to save to {file_path}")
        return

    logger.info(f"Saving {df.shape[0]} data to {file_path}")

    try:
        # Create the parent directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Save the DataFrame to Parquet
        df.to_parquet(file_path, **kwargs)

        logger.info(f"Save Success: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving DataFrame to {file_path}: {str(e)}")
        raise
