#!/usr/bin/env python3
import getpass
import json
import subprocess
import sys


# This function creates a Docker Config, which will be used to store the IP address of the NAS and the name of our assigned database. This information is stored within the Swarm manager (the HMI Pi) to avoid hard-coding it in each of the container scripts.
def create_docker_config(name, data):
    try:
        subprocess.run(["docker", "config", "create", name, "-"], input=data, text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        # If the "docker config create" command failed due to the config file already existing, then we can just use the existing config file.
        if ("AlreadyExists" in e.stderr) or ("code = 2" in e.stderr):
            print("Config already exists, skipping creation.")
        # Otherwise, if the failure was due to something else, then we need to abort the configuration and deployment of the Swarm.
        else:
            print("There was a problem creating the config file:")
            print(e.stderr)
            sys.exit(1)

# This function creates a Docker Secret to store sensitive information. For this project, we use two secrets to store the username and password needed to access our assigned database.
def create_docker_secret(name, value):
    try:
        subprocess.run(["docker", "secret", "create", name, "-"], input=value, text=True, check=True)
    except subprocess.CalledProcessError as e:
        # If the "docker secret create" command failed due to the secret already existing, then we can just use the existing secret.
        if ("AlreadyExists" in e.stderr) or ("code = 2" in e.stderr):
            print("Secret already exists, skipping creation.")
        # Otherwise, if the failure was due to something else, then we need to abort the configuration and deployment of the Swarm.
        else:
            print("There was a problem creating the config file:")
            print(e.stderr)
            sys.exit(1)


def main():
    print("NAS Database Configuration")
    print("--------------------------")

    # Propmt the user to enter the following four credentials. These credentials are used to give the container scripts access to our assigned database on the NAS.
    nas_ip = input("NAS IP address: ").strip()
    db_name = input("Database name: ").strip()
    db_user = input("Database username: ").strip()
    db_pass = getpass.getpass("Database password: ")
    # getpass() prevents the user's input from being displayed in the terminal.

    # Check that all four credentials were provided. If not, then we cannot continue configuring or deploying the Swarm.
    if not all([nas_ip, db_name, db_user, db_pass]):
        print("All fields are required.")
        sys.exit(1)

    # Construct a JSON-formatted string that will become the config file.
    config = {
        "nas_ip": nas_ip,
        "database": db_name
    }
    config_json = json.dumps(config)

    # Create the config file.
    print("\nCreating Docker configuration...")
    create_docker_config("nas_config", config_json)

    # Create the secrets.
    print("Creating Docker secrets...")
    create_docker_secret("nas_username", db_user)
    create_docker_secret("nas_password", db_pass)

    print("\nConfiguration successfully created!")
if __name__ == "__main__":
    main()
