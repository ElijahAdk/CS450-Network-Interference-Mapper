import getpass
import json
import subprocess
import sys

def create_docker_config(name, data):
    subprocess.run(["docker", "config", "create", name, "-"], input=data, text=True, check=True)
def create_docker_secret(name, value):
    subprocess.run(["docker", "secret", "create", name, "-"], input=value, text=True, check=True)

def main():
    print("NAS Database Configuration")
    print("--------------------------")

    nas_ip = input("NAS IP address: ").strip()
    database = input("Database name: ").strip()
    username = input("Database username: ").strip()
    password = getpass.getpass("Database password: ")

    if not all([nas_ip, database, username, password]):
        print("All fields are required.")
        sys.exit(1)

    config = {
        "nas_ip": nas_ip,
        "database": database
    }
    config_json = json.dumps(config)

    print("\nCreating Docker configuration...")
    create_docker_config("nas_config", config_json)

    print("Creating Docker secrets...")
    create_docker_secret("nas_username", username)
    create_docker_secret("nas_password", password)

    print("\nConfiguration successfully created!")

if __name__ == "__main__":
    main()
