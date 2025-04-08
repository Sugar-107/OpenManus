from typing import Dict, List, Optional, Union

import mysql.connector

from app.tool.base import BaseTool


class MySQLTool(BaseTool):
    """A tool for executing MySQL database operations."""

    name: str = "mysql"
    description: str = (
        "Executes MySQL database operations including queries and data manipulation."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "MySQL server host address",
            },
            "user": {
                "type": "string",
                "description": "MySQL username",
            },
            "password": {
                "type": "string",
                "description": "MySQL password",
            },
            "database": {
                "type": "string",
                "description": "Database name to connect to",
            },
            "query": {
                "type": "string",
                "description": "SQL query to execute",
            },
            "params": {
                "type": "array",
                "description": "Query parameters for prepared statements",
                "items": {"type": ["string", "number", "boolean", "null"]},
            },
        },
        "required": ["host", "user", "password", "database", "query"],
    }

    async def execute(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        query: str,
        params: Optional[List[Union[str, int, float, bool, None]]] = None,
    ) -> Dict:
        """
        Executes a MySQL query with optional parameters.

        Args:
            host: MySQL server host address
            user: MySQL username
            password: MySQL password
            database: Database name
            query: SQL query to execute
            params: Optional parameters for prepared statements

        Returns:
            Dict containing query results or error message
        """
        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )

            cursor = connection.cursor(dictionary=True)

            # Execute query with parameters if provided
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Fetch results
            if query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
                results = cursor.fetchall()
                return {
                    "success": True,
                    "results": results,
                    "rowcount": cursor.rowcount,
                }
            else:
                # For non-SELECT queries, commit changes
                connection.commit()
                return {
                    "success": True,
                    "message": f"Query executed successfully. Affected rows: {cursor.rowcount}",
                }

        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}
        finally:
            if "cursor" in locals():
                cursor.close()
            if "connection" in locals():
                connection.close()
