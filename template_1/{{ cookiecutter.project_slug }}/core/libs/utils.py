import yaml
from pathlib import Path
import pandas as pd
import requests

from prefect import task
from prefect.logging import get_run_logger
from prefect.variables import Variable
from prefect.artifacts import create_table_artifact


@task(
    name="update_data_artifact",
    description="Update data artifact",
    task_run_name="update-data-artifact",
)
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


@task(
    name="save_artifact",
    description="Save artifact in Prefect",
    task_run_name="save-artifact-{key_name}",
)
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
    name="get_data_api",
    description="Get data from API",
    task_run_name="get-data-api-{url}",
)
def get_data_api(url: str, **kwargs) -> dict:
    """
    Get data from API

    Args:
        url: URL of the API
        kwargs: additional parameters for the request

    Returns:
        dict: JSON response from the API
    """
    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()["results"]

    except Exception as e:
        raise ValueError(f"Error fetching data from API: {str(e)}")


@task(
    name="load_data",
    description="Load data from various sources",
    task_run_name="load-data-{file_path}",
)
def load_data(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Load data from various file_paths (API endpoint, CSV or Parquet file).

    The function automatically detects the type of file_path based on the file_path parameter:
    - file_path ending with '.csv' are loaded as CSV files
    - file_path ending with '.parquet' or '.pq' are loaded as Parquet files
    - file_path ending with '.json' are loaded as JSON files

    Args:
        file_path: file_path of the data (URL or file path)
        kwargs: Additional parameters for the loading function

    Returns:
        Pandas DataFrame containing the loaded data
    """
    # Get logger
    logger = get_run_logger()

    logger.info(f"Loading data from {file_path}")

    try:
        # Detect the file_path type
        if file_path.endswith(".csv"):
            logger.info(f"Detected CSV file: {file_path}")
            response = pd.read_csv(file_path, **kwargs)

        elif file_path.endswith((".parquet", ".pq")):
            logger.info(f"Detected Parquet file: {file_path}")
            response = pd.read_parquet(file_path, **kwargs)

        elif file_path.endswith(".json"):
            logger.info(f"Detected JSON file: {file_path}")
            response = pd.read_json(file_path, **kwargs)

        else:
            raise ValueError(
                f"Unsupported file_path type for {file_path}. Supported types: JSON, CSV, Parquet"
            )

        # Check if the response is empty
        if response.empty:
            logger.warning(f"No data found at {file_path}")
            return pd.DataFrame()
        else:
            logger.info(
                f"Data loaded: {len(response)} rows, {response.columns.size} columns"
            )
            return response

    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        raise


@task(
    name="save_data",
    description="Save DataFrame to file",
    task_run_name="save-data-{file_path}",
)
def save_data(df: pd.DataFrame, file_path: str, **kwargs) -> str:
    """
    Save a DataFrame to a file.

    Args:
        df: DataFrame to save
        file_path: Path to save the file
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

        if file_path.endswith(".csv"):
            df.to_csv(file_path, **kwargs)
        elif file_path.endswith((".parquet", ".pq")):
            df.to_parquet(file_path, **kwargs)

        logger.info(f"Save Success: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving DataFrame to {file_path}: {str(e)}")
        raise


@task(
    name="get_data_schema",
    description="Get data schema from YAML file",
    task_run_name="get-data-schema-{file_path}",
)
def get_data_schema(file_path: str, table_name: str) -> dict:
    """
    Get data schema from YAML file

    Args:
        file_path: Path to the YAML file
        table_name: Name of the table to get the schema for

    Returns:
        dict: Schema of the table
    """
    # Get logger
    logger = get_run_logger()

    # Load the YAML file
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    # Find the table in the YAML file
    for table in config["datamodel"]["tables"]:
        if table["name"] == table_name:
            return table

    logger.error(f"Table {table_name} not found in {file_path}")
    return {}


@task(
    name="upudate_columns_types",
    description="Update columns types",
    task_run_name="update-columns-types",
)
def update_columns_types(df: pd.DataFrame, data_schema: dict) -> pd.DataFrame:
    """
    Update columns types based on the schema from config YAML file.

    Args:
        df: DataFrame to update
        data_schema: Schema of the table to update

    Returns:
        DataFrame with updated column types
    """

    # update types
    for col in data_schema["columns"]:
        col_name = col["name"]
        col_type = col["type"]

        if col_name in df.columns:
            if col_type == "integer":
                df[col_name] = df[col_name].astype(int)
            elif col_type == "float":
                df[col_name] = df[col_name].astype(float)
            elif col_type == "string":
                df[col_name] = df[col_name].astype(str)
            elif col_type == "datetime":
                df[col_name] = pd.to_datetime(df[col_name], errors="coerce")
            elif col_type == "bool":
                df[col_name] = df[col_name].astype(bool)

    return df
