#!/bin/bash


docker compose -f build/compose.yaml --env-file build/docker.env down
# Or `docker compose -f build/compose.yaml --env-file docker.env down --rmi all` ro remove the image as well.
