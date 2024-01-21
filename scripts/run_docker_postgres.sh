#!/bin/bash

user=admin@admin.admin
password=password
postgres_container_name=postgres-db
postgres_user=postgres


if docker run --detach --publish 5432:5432 --hostname my-postgres --name $postgres_container_name --env POSTGRES_USER=$postgres_user --env POSTGRES_PASSWORD=$password postgres 2> /dev/null; then
    echo 'Built and started postgres from scratch'
else
    docker restart postgres &> /dev/null;
    echo 'Started postgres from existing image'
fi

if docker run --detach --publish 82:80 --hostname my-pgadmin --name pgadmin --env PGADMIN_DEFAULT_EMAIL=$user --env PGADMIN_DEFAULT_PASSWORD=$password dpage/pgadmin4 2> /dev/null; then
    echo 'Built and started dpage/pgadmin4 from scratch'
else
    docker restart dpage/pgadmin4 &> /dev/null;
    echo 'Started dpage/pgadmin4 from existing image'
fi

if docker run --detach --publish 83:8080 --hostname my-adminer --name adminer adminer 2> /dev/null; then
    echo 'Built and started adminer from scratch'
else
    docker restart adminer &> /dev/null;
    echo 'Started adminer from existing image'
fi


echo 'Serving HTTP on 127.0.0.1 port 82 (http://127.0.0.1:82/)'
echo "Username:       "$user""
echo "Password:       "$password""
echo "Postgres Host:  "$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $postgres_container_name)""
echo "Postgres user:  "$postgres_user""
