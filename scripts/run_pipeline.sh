#!/bin/bash


docker compose -f build/compose.yaml --env-file build/docker.env up -d --build
# To enter shell in a container `docker exec -it <container-name> sh`
# To rebuild this image you must use `docker compose -f build/compose.yaml build` or `docker compose -f build/compose.yaml up --build` to run the image as well.
