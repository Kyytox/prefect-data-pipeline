import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

# Prefect
from prefect import task

# Paths
from core.config.path import PATH_DATA_RAW, PATH_DATA_PROCESSED, PATH_CONFIG_SCHEMA

# Utils
from core.libs.utils import (
    load_data,
    save_data,
    get_data_schema,
    upd_data_artifact,
    update_columns_types,
)


@task(
    name="nb_launches_by_country",
    task_run_name="nb-launches-by-country",
    description="Get number of launches by country",
)
def nb_launches_by_country(table: pa.Table) -> pa.Table:
    """
    Get number of launches by country
    Get number of successful launches by country

    Returns:
        pa.Table: Table with columns (country, nb_launch, nb_success)
    """
    # Extract unique countries
    countries = pc.unique(table["country"])

    # Create a list to store the results
    results = []

    # For each country, count total launches and successful launches
    for country in countries:
        country_str = country.as_py()

        # Filter data for this country
        mask_country = pc.equal(table["country"], country)
        country_data = table.filter(mask_country)

        # Count total launches for this country
        nb_launch = country_data.num_rows

        # Count successful launches for this country
        # Convert status to lowercase for case-insensitive comparison
        status_lower = pc.utf8_lower(country_data["status"])
        success_mask = pc.equal(status_lower, "success")
        success_data = country_data.filter(success_mask)
        nb_success = success_data.num_rows if success_data else 0

        # Add to results
        results.append(
            {"country": country_str, "nb_launch": nb_launch, "nb_success": nb_success}
        )

    # Convert the results to a PyArrow Table
    if results:
        return pa.Table.from_pylist(results)
    else:
        # Create an empty table with the right schema
        return pa.table(
            {
                "country": pa.array([], type=pa.string()),
                "nb_launch": pa.array([], type=pa.int64()),
                "nb_success": pa.array([], type=pa.int64()),
            }
        )


@task(
    name="task_transform",
    task_run_name="task-transform",
    description="Transform data from data/raw",
)
def task_transform():
    """
    Task to transform data from raw data
    """

    file_src = f"{PATH_DATA_RAW}/rockets_launches.parquet"
    file_dest = f"{PATH_DATA_PROCESSED}/rockets_launches_stats.parquet"

    # Get schema of data
    data_schema = get_data_schema(PATH_CONFIG_SCHEMA, "processed")

    # Load data
    launch_table = load_data(file_src)

    # Calculate launches by country
    table = nb_launches_by_country(launch_table)

    # Update columns types
    table = update_columns_types(table, data_schema)

    # Save country stats
    save_data(
        table=table,
        file_path=file_dest,
    )

    # Add country stats to artifact
    upd_data_artifact(
        info=f"Country launch statistics",
        data=f"{table.num_rows} countries analyzed",
    )
