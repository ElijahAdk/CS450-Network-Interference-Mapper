#!/bin/bash

set -e

echo "Starting deployment..."

# Collect configuration and create Docker resources
python3 configure.py

# Deploy the Docker Swarm stack
docker stack deploy \
    -c docker-compose.yml \
    nas_application

echo "Deployment completed!"
