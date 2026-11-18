#!/bin/bash

# Configure this Shell script to terminate immediately if any command returns a non-zero exit status.
set -e

echo "Starting deployment..."

# Collect configuration information from the user and create the associated Docker config file and secrets.
python3 configure.py

# Deploy the Docker Swarm stack.
docker stack deploy -c compose.yaml network_interference_mapper

echo "Deployment completed!"
