# Base dockerfile for executing brain-computer-interface's python packages.
# Note:
# It's discourage to run the project's tests in a docker container, since the tests use docker command.

FROM python:3.11-slim-buster

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD brain_computer_interface/ /brain_computer_interface

CMD bash
