#!\python3\Scripts\python

"""postgr_conn.py: Connect to PostgreSQL database server, get database cursor."""
__author__ = "Peter Kovacs - 29.04.2021."

def postgres_connection(database):

    try:
        # Import psycopg2 library from virtual-environment
        import psycopg2
    except ModuleNotFoundError as error:
        raise error('No PostgreSQL extension')

    try:
        # Connect to the test-database
        connection = psycopg2.connect(user=database,
                                    password="H-8_3SARM_wknvE7W8A4eEcHAzIJ-n2F",
                                    host="tai.db.elephantsql.com",
                                    port="5432",
                                    database=database)
        return connection.cursor()

    except:
        raise NameError('No Database Connection')