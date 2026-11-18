#!/usr/bin/env python3
import json
import mysql.connector
import socket
import sys
import time
from datetime import datetime, timezone

HOST_NAME = "logger"  # the hostname of this Logger service's container
HOST_PORT = 41000      # the port that the Logger service listens on

# INSERT query for inserting data values into this Logger service's database table.
insert_query = """
    INSERT INTO <table_name> (timestamp, link_quality, signal_level, magnet_x, magnet_y, magnet_z)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

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

def main():
    # Get the configuration information needed to access the NAS.
    DB_CONFIG = get_database_config()

    # Create and bind a socket to use for communication with the Data Polling service.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
        data_socket.bind((HOST_NAME, HOST_PORT))

        # Listen for incoming connections.
        data_socket.listen()

        # Accept an incoming connection.
        data_conn, data_addr = data_socket.accept()
        with data_conn:
            print(f"Connection accepted from {data_addr}.")

            # Continuously check if any new data has been received.
            while True:
                # Read any available bytes from the socket's buffer.
                data_bytes = data_conn.recv(4096)

                # Check if the connection has been closed (which causes socket.recv() to return an empty bytes object).
                if not data_bytes:
                    break

                # Reconstruct the transmitted string from the received bytes.
                data_string = data_bytes.decode('utf-8')

                # Slice the string to extract each data point.
                data_vals = data_string.split(" ")
                print(f"Timestamp: {time.strftime('%X')}\nLink Quality: {data_vals[0]}/70\nSignal Level: {data_vals[1]} dBm\nMagnetometer: ({data_vals[2]} µT, {data_vals[3]} µT, {data_vals[4]} µT)")

                # Connect to the NAS database and create a cursor to interact with this Logger service's database table.
                try:
                    with (mysql.connector.connect(**DB_CONFIG) as nas_conn, nas_conn.cursor() as nas_cursor):
                        print("Connected to NAS MariaDB.\nAttempting to insert received data...")

                        # Execute the INSERT query to create a new record to store the received data.
                        nas_cursor.execute(insert_query, (datetime.now(timezone.utc), int(data_vals[0]), int(data_vals[1]), float(data_vals[2]), float(data_vals[3]), float(data_vals[4])))
                        nas_conn.commit()
                        print("Data inserted successfully.\nDisconnecting from NAS MariaDB.")
                        # We can disconnect from the NAS between queries to conserve the NAS's resources, especially since these queries are performed relatively infrequently (i.e. one query every 5+ seconds).
                # If an error occurred regarding the NAS, report the error.
                except mysql.connector.Error as err:
                    print(f"[ERROR] Database error: {err}")
if __name__ == "__main__":
    main()
