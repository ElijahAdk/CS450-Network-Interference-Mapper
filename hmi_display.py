import os
import sys
import json
import time
import mysql.connector
from mysql.connector import Error

poll_interval = 5.0

sensor_tables = [
    "sense_hat_1",
    "sense_hat_2",
    "sense_hat_3"
]

# Set how many of the newest records for each table to display
records_to_display = 3

# Retrieve the NAS MariaDB connection configuration information from the Docker config file and the Docker secrets. We use a Docker config file and Docker secrets to avoid hard-coding the IP address of the NAS, the name of our assigned database, and the log-in credentials needed to access the database (i.e. username and password).
def get_database_config():
    # Read the config file to get the NAS IP address and database name.
    with open("/app/config.json", "r") as f:
        config = json.load(f)
    # Check that the config file could be read successfully. If so, check that the stored information was successfully extracted.
    if not config:
        print("Config file could not be read.")
        sys.exit(1)
    else:
        if not config["nas_ip"]:
            print("NAS IP address could not be retrieved from the config file.")
            sys.exit(1)
        elif not config["database"]:
            print("Database name could not be retrieved from the config file.")
            sys.exit(1)

    # Retrieve the database username and password from Docker secrets.
    with open("/run/secrets/nas_username", "r") as f:
        username = f.read().strip()
    with open("/run/secrets/nas_password", "r") as f:
        password = f.read().strip()

    # Check that the username and password were successfully retrieved from the Docker secrets.
    if not username:
        print("Database username could not be found.")
        sys.exit(1)
    elif not password:
        print("Database password could not be found.")
        sys.exit(1)

    # Return a dictionary object containing the retrieved information.
    return {
        "host": config["nas_ip"],
        "port": 3306,
        "database": config["database"],
        "user": username,
        "password": password
    }

class NASConnection:

    def __init__(self):
        self.config = get_database_config()

    def connect(self):

        return mysql.connector.connect(
            **self.config,
            connect_timeout= 3
        )

nas = NASConnection()

def request_sensor_data(connection):
    results = {}
    # Query each sensor table for the newest records
    for table in sensor_tables:
        try:
            select_query = f"""SELECT * FROM '{table}' ORDER BY 'timestamp' DESC LIMIT %s"""

            cursor = connection.cursor(dictionary=True)
            cursor.execute(select_query, (records_to_display,))
            results[table] = cursor.fetchall()
            cursor.close()

        except Error as error:
            print(f"Error querying {table}: {error}")
            results[table] = []
            
    return results

def display_table(results):

    # Clear terminal
    print("\033[2J\033[H", end="")

    print("DATA MONITORING SYSTEM")
    print(f"\nLast updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n" + "_" * 105)

    for table, records in results.items():
        
        print("\n")
        print(f"Data from: {table}")
        # Column headers
        print(
            f"{'Timestamp':<25}"
            f"{'Link Quality':<16}"
            f"{'Signal Level':<16}"
            f"{'Magnet X':<15}"
            f"{'Magnet Y':<15}"
            f"{'Magnet Z':<15}"
        )
        print(f"\n" + "-" * 105)

        if not records:
            print("No records available.")
            continue

        for record in records:
            # Entries
            print(
                f"{str(record['timestamp']):<25}"
                f"{str(record['link_quality']):<16}"
                f"{str(record['signal_level'] + 'dBm'):<16}" 
                f"{str(record['magnet_x'] + 'uT'):<15}" 
                f"{str(record['magnet_y'] + 'uT'):<15}"
                f"{str(record['magnet_z'] + 'uT'):<15}"
            )
        print(f"\n" + "=" * 105)

    print("\n" + "_" * 105)
    print(f"Refreshing in {poll_interval} seconds...")

def main():

    print("Starting Monitoring System...")

    try:
        while True:
            connection = None

            try:
                connection = nas.connect()
                results = request_sensor_data(connection)
                display_table(results)

            except (Error, OSError, RuntimeError) as error:
                print("\nUnable to communicate with NAS.")
                print(f"Error: {error}")

            finally:
                if connection and connection.is_connected():
                    connection.close()

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        print("\n Shutting down Monitoring System...")

if __name__ == "__main__":
    main()
