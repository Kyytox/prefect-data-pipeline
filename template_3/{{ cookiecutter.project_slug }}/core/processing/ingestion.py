import pyarrow as pa

# Prefect
from prefect import task

# Paths
from core.config.path import URL_API, PATH_CONFIG_SCHEMA

# Utils
from core.libs.utils import (
    get_data_api,
    upd_data_artifact,
    get_data_schema,
    update_columns_types,
)
from core.libs.db_utils import save_to_postgres


def get_nested_value(item, path, default=None):
    """
    Recovers a value from a dictionary by following a point path.

    Args:
        item (dict): Dict from which to extract the value
        path (str): Path to the value, separated by points
        default: Default value to return if the path does not exist

    Returns:
        The value of the path in the dictionary or the default value
    """
    keys = path.split(".")
    current = item

    try:
        for key in keys:
            if current is None:
                return default
            if isinstance(current, dict):
                current = current.get(key, None)
            else:
                return default
        return current
    except (KeyError, TypeError, AttributeError):
        return default


@task(
    name="filter_columns",
    task_run_name="filter-columns",
    description="Filter columns from data",
)
def filter_columns(json_data, data_schema):
    """
    Get necessary columns from the data

    Args:
        data (dict): Data to filter
        columns (list): List of columns to keep
    """

    # Create a dictionary to map link
    corresp_dict = {col["name"]: col["link"] for col in data_schema["columns"]}

    data = []

    # Loop through the JSON data and extract the necessary fields
    for item in json_data:
        filtered_item = {}
        for new_name, old_name in corresp_dict.items():
            # Extract the value from the nested structure
            filtered_item[new_name] = get_nested_value(item, old_name)

        data.append(filtered_item)

    # Convert the list of dictionaries to a PyArrow Table
    return pa.Table.from_pylist(data)


@task(
    name="task_ingestion",
    task_run_name="task-ingestion",
    description="Ingest data from API and store in PostgreSQL",
)
def task_ingestion():
    """
    Task to ingest data from API

    - Get data from API
    - Retrieve necessary columns
    - Update columns types
    - Save data to PostgreSQL database
    """

    file_src = f"{URL_API}"
    schema_name = "public"
    table_name = "raw_rockets"

    # Get schema of data
    data_schema = get_data_schema(
        file_path=PATH_CONFIG_SCHEMA, table_name="raw_rockets"
    )

    # Load data -> returns a JSON file
    json_data = get_data_api(file_src)

    # Collect necessary columns
    table = filter_columns(json_data, data_schema)

    # Update columns types
    table = update_columns_types(table, data_schema)

    # Convert PyArrow table to pandas DataFrame for database storage
    df = table.to_pandas()

    # Save data to PostgreSQL
    save_to_postgres(
        df=df, table_name=table_name, schema=schema_name, if_exists="append"
    )

    # Update artifact
    upd_data_artifact(
        info=f"Ingestion data from {file_src} to PostgreSQL",
        data=f"{len(df)} rows and {len(df.columns)} columns saved to {schema_name}.{table_name}",
    )
