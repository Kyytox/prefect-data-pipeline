import yaml
from pathlib import Path
import pyarrow as pa
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow.dataset as ds
import requests
import json
from typing import Dict, List, Any, Union

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
def load_data(file_path: str, **kwargs) -> pa.Table:
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
        PyArrow Table containing the loaded data
    """
    # Get logger
    logger = get_run_logger()

    logger.info(f"Loading data from {file_path}")

    try:
        # Detect the file_path type
        if file_path.endswith(".csv"):
            logger.info(f"Detected CSV file: {file_path}")
            read_options = kwargs.get("read_options", csv.ReadOptions())
            parse_options = kwargs.get("parse_options", csv.ParseOptions())
            convert_options = kwargs.get("convert_options", csv.ConvertOptions())

            table = csv.read_csv(
                file_path,
                read_options=read_options,
                parse_options=parse_options,
                convert_options=convert_options,
            )

        elif file_path.endswith((".parquet", ".pq")):
            logger.info(f"Detected Parquet file: {file_path}")
            table = pq.read_table(file_path)

        elif file_path.endswith(".json"):
            logger.info(f"Detected JSON file: {file_path}")
            # PyArrow doesn't have direct JSON file support, so we read and convert
            with open(file_path, "r") as f:
                data = json.load(f)

            # Convert JSON to PyArrow Table
            if isinstance(data, list) and len(data) > 0:
                # Assuming all items have the same structure
                table = pa.Table.from_pylist(data)
            else:
                logger.warning(f"Empty or invalid JSON data in {file_path}")
                return pa.Table.from_pylist([])

        else:
            raise ValueError(
                f"Unsupported file_path type for {file_path}. Supported types: JSON, CSV, Parquet"
            )

        # Check if the table is empty
        if table.num_rows == 0:
            logger.warning(f"No data found at {file_path}")
            return pa.Table.from_pylist([])
        else:
            logger.info(
                f"Data loaded: {table.num_rows} rows, {len(table.column_names)} columns"
            )
            return table

    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        raise


@task(
    name="save_data",
    description="Save PyArrow Table to file",
    task_run_name="save-data-{file_path}",
)
def save_data(table: pa.Table, file_path: str, **kwargs) -> str:
    """
    Save a PyArrow Table to a file.

    Args:
        table: PyArrow Table to save
        file_path: Path to save the file
    """
    # Get logger
    logger = get_run_logger()

    if table.num_rows == 0:
        logger.warning(f"Table is empty, nothing to save to {file_path}")
        return

    logger.info(f"Saving {table.num_rows} data to {file_path}")

    try:
        # Create the parent directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        if file_path.endswith(".csv"):
            # Write to CSV
            csv.write_csv(table, file_path, **kwargs)
        elif file_path.endswith((".parquet", ".pq")):
            # Write to Parquet
            pq.write_table(table, file_path, **kwargs)

        logger.info(f"Save Success: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving Table to {file_path}: {str(e)}")
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
def update_columns_types(table: pa.Table, data_schema: dict) -> pa.Table:
    """
    Update columns types based on the schema from config YAML file.

    Args:
        table: PyArrow Table to update
        data_schema: Schema of the table to update

    Returns:
        PyArrow Table with updated column types
    """
    # Convert table to dict of arrays for modification
    data_dict = {
        col_name: table[col_name].to_numpy() for col_name in table.column_names
    }

    # Update types based on schema
    for col in data_schema["columns"]:
        col_name = col["name"]
        col_type = col["type"]

        if col_name in table.column_names:
            # Create a new PyArrow type based on the schema
            if col_type == "integer":
                data_dict[col_name] = pa.array(data_dict[col_name], type=pa.int64())
            elif col_type == "float":
                data_dict[col_name] = pa.array(data_dict[col_name], type=pa.float64())
            elif col_type == "string":
                data_dict[col_name] = pa.array(data_dict[col_name], type=pa.string())
            elif col_type == "datetime":
                # Convert to timestamp, handling potential parsing errors
                try:
                    data_dict[col_name] = pa.array(
                        data_dict[col_name], type=pa.timestamp("ns")
                    )
                except:
                    # For invalid datetime values, keep as string
                    data_dict[col_name] = pa.array(
                        data_dict[col_name], type=pa.string()
                    )
            elif col_type == "bool":
                data_dict[col_name] = pa.array(data_dict[col_name], type=pa.bool_())

    # Recreate the table with updated arrays
    return pa.Table.from_arrays(
        [data_dict[col_name] for col_name in table.column_names],
        names=table.column_names,
    )
