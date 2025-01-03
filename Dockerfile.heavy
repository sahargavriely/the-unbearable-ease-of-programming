# Base dockerfile for executing brain-computer-interface's python packages.
# Note:
# It's discourage to run the project's tests in this docker container, since the tests use docker command.

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-bookworm

# For docker compose health checks
RUN apt-get update && apt-get install -y netcat-traditional

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# # Making sure we have the same time as our local machine (mainly help with tests)
# VOLUME /etc/localtime /etc/localtime ro
# VOLUME /etc/timezone /etc/timezone ro
# VOLUME usr/share/zoneinfo usr/share/zoneinfo ro

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY brain_computer_interface/ /brain_computer_interface

EXPOSE 5000
EXPOSE 8000

CMD ["bash"]
