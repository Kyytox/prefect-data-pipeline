"""
Database utilities for PostgreSQL connection and operations
"""

import os
from sqlalchemy import create_engine
from prefect.blocks.system import Secret


def get_db_connection_string():
    """
    Get database connection string from environment variables or Prefect secrets

    Returns:
        str: PostgreSQL connection string
    """
    try:
        # Try to get connection string from Prefect Secret
        db_secret = Secret.load("postgres-connection")
        return db_secret.get()
    except:
        # Fallback to environment variables
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DBT_ENV_SECRET_DB_PASSWORD", "root")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "db_azert")

        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_db_engine():
    """
    Get SQLAlchemy engine for PostgreSQL

    Returns:
        sqlalchemy.engine.Engine: Database engine
    """
    conn_string = get_db_connection_string()
    return create_engine(conn_string)


def save_to_postgres(df, table_name, schema="raw", if_exists="append"):
    """
    Save data to PostgreSQL database

    Args:
        df (pd.DataFrame): DataFrame to save
        table_name (str): Table name
        schema (str): Schema name
        if_exists (str): How to behave if table exists (replace, append, fail)
    """
    engine = get_db_engine()
    df.to_sql(
        name=table_name, con=engine, schema=schema, if_exists=if_exists, index=False
    )
