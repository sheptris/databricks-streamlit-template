"""
Databricks connection utilities for Streamlit apps.

This module provides helper functions to connect to Databricks resources
such as SQL warehouses and Unity Catalog tables.
"""

import os
from typing import Optional
import pandas as pd


def get_databricks_connection():
    """
    Create a connection to Databricks SQL warehouse.

    Returns:
        connection object if successful, None otherwise

    Example:
        >>> connection = get_databricks_connection()
        >>> cursor = connection.cursor()
        >>> cursor.execute("SELECT * FROM catalog.schema.table LIMIT 10")
        >>> df = cursor.fetchall_arrow().to_pandas()
    """
    try:
        from databricks import sql

        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        return connection
    except ImportError:
        print("databricks-sql-connector not installed. Run: pip install databricks-sql-connector")
        return None
    except Exception as e:
        print(f"Error connecting to Databricks: {e}")
        return None


def query_databricks_table(
    catalog: str,
    schema: str,
    table: str,
    limit: Optional[int] = None,
    filters: Optional[str] = None
) -> Optional[pd.DataFrame]:
    """
    Query a Databricks table and return as pandas DataFrame.

    Args:
        catalog: Unity Catalog name
        schema: Schema name
        table: Table name
        limit: Optional row limit
        filters: Optional WHERE clause (without the WHERE keyword)

    Returns:
        pandas DataFrame or None if query fails

    Example:
        >>> df = query_databricks_table(
        ...     catalog="main",
        ...     schema="sales",
        ...     table="transactions",
        ...     limit=1000,
        ...     filters="date >= '2024-01-01'"
        ... )
    """
    connection = get_databricks_connection()
    if connection is None:
        return None

    try:
        query = f"SELECT * FROM {catalog}.{schema}.{table}"

        if filters:
            query += f" WHERE {filters}"

        if limit:
            query += f" LIMIT {limit}"

        cursor = connection.cursor()
        cursor.execute(query)
        df = cursor.fetchall_arrow().to_pandas()
        cursor.close()
        connection.close()

        return df
    except Exception as e:
        print(f"Error querying table: {e}")
        return None


def execute_sql_query(query: str) -> Optional[pd.DataFrame]:
    """
    Execute a custom SQL query and return results as DataFrame.

    Args:
        query: SQL query string

    Returns:
        pandas DataFrame or None if query fails

    Example:
        >>> query = '''
        ...     SELECT region, SUM(sales) as total_sales
        ...     FROM catalog.schema.sales
        ...     GROUP BY region
        ... '''
        >>> df = execute_sql_query(query)
    """
    connection = get_databricks_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        df = cursor.fetchall_arrow().to_pandas()
        cursor.close()
        connection.close()

        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def get_workspace_client():
    """
    Create a Databricks Workspace client for accessing workspace resources.

    Returns:
        WorkspaceClient object or None

    Example:
        >>> client = get_workspace_client()
        >>> # List all clusters
        >>> clusters = client.clusters.list()
        >>> # Access workspace files
        >>> files = client.workspace.list("/Workspace/Users/your-email")
    """
    try:
        from databricks.sdk import WorkspaceClient

        client = WorkspaceClient(
            host=os.getenv("DATABRICKS_HOST"),
            token=os.getenv("DATABRICKS_TOKEN")
        )
        return client
    except ImportError:
        print("databricks-sdk not installed. Run: pip install databricks-sdk")
        return None
    except Exception as e:
        print(f"Error creating workspace client: {e}")
        return None
