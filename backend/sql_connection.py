import mysql.connector

__cnx = None  # Global variable for the MySQL connection

def get_sql_connection():
    global __cnx
    if __cnx is None:  # Fix the missing space after 'if'
        try:
            __cnx = mysql.connector.connect(
                user='root',                # Default WAMP MySQL user
                password='nethma123',       # Default WAMP password
                host='127.0.0.1',           # Localhost
                database='nvds_grocerry_store',  # Replace with your database name
                port=3306                   # Default MySQL port
            )
            print("Connection established successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise  # Reraise the exception to let the caller handle it
    return __cnx
