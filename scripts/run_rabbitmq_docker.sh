#!/bin/bash


# docker run --detach -p 5672:5672 -p 15672:15672 --hostname my-rabbit --name rabbit rabbitmq:management
# username & password: guest

# if docker run --detach --publish 5672:5672 --hostname my-rabbit --name rabbit rabbitmq 2> /dev/null; then
if docker run --detach -p 5672:5672 -p 15672:15672 --hostname my-rabbit --name rabbit rabbitmq:management 2> /dev/null; then
    echo 'Built and started rabbitmq from scratch'
else
    docker restart rabbit &> /dev/null;
    echo 'Started rabbitmq from existing image'
fi

echo 'Serving HTTP on 127.0.0.1 port 15672 (http://127.0.0.1:15672/)'
echo 'Username: "guest".'
echo 'Password: "guest".'
