# common/db_connection.py
import mysql.connector

def connect(host="localhost", user="root", password="emma", database="chessdb"):
    """
    Establishes a connection to the MySQL database.

    Parameters:
        host (str): Hostname of the MySQL server.
        user (str): Username for the MySQL connection.
        password (str): Password for the MySQL connection.
        database (str): Name of the database to connect to.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection: MySQL database connection.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Database connection successful.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
