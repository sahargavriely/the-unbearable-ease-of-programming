#!/bin/bash


docker-compose --env-file docker.env up -d --build
# To enter shell in a container `docker exec -it <container-name> sh`
# To rebuild this image you must use `docker-compose build` or `docker-compose up --build` to run the image as well.
