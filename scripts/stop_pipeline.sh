#!/bin/bash


docker-compose --env-file docker.env down
# Or `docker-compose --env-file docker.env down --rmi all` ro remove the image as well.
