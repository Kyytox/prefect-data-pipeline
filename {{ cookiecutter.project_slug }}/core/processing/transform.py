import pandas as pd

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
def nb_launches_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get number of launches by country
    Get number of successful launches by country

    Returns:
        pd.DataFrame: DataFrame with columns (country, nb_launch, nb_success)
    """
    # Group by country and count total launches
    country_launches = df.groupby("country").size().reset_index(name="nb_launch")

    # Filter for successful launches and count by country
    success_launches = (
        df[df["status"].str.lower() == "success"]
        .groupby("country")
        .size()
        .reset_index(name="nb_success")
    )

    # Merge the two dataframes
    result = pd.merge(country_launches, success_launches, on="country", how="left")

    # Rename country column and fill NaN values with 0
    result["nb_success"] = result["nb_success"].fillna(0).astype(int)

    return result


@task(
    name="task_transform",
    task_run_name="task-transform",
    description="Transform data from data/raw",
)
def task_transform():
    """
    Task to ingest data from API
    """

    file_src = f"{PATH_DATA_RAW}/rockets_launches.parquet"
    file_dest = f"{PATH_DATA_PROCESSED}/rockets_launches_stats.parquet"

    # Get schema of data
    data_schema = get_data_schema(PATH_CONFIG_SCHEMA, "processed")

    # Load data
    df_launch = load_data(file_src)

    # Calculate launches by country
    df = nb_launches_by_country(df_launch)

    # Update columns types
    df = update_columns_types(df, data_schema)

    # Save country stats
    save_data(
        df=df,
        file_path=file_dest,
        index=False,
    )

    # Add country stats to artifact
    upd_data_artifact(
        info=f"Country launch statistics",
        data=f"{len(df)} countries analyzed",
    )
