[![github-workflow](https://github.com/sahargavriely/the-unbearable-ease-of-programming/actions/workflows/github-action.yml/badge.svg)](https://github.com/sahargavriely/the-unbearable-ease-of-programming/actions/workflows/github-action.yml)
[![codecov](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming/graph/badge.svg?token=W0V7MR7T8S)](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming)
[![readthedocs](https://readthedocs.org/projects/the-unbearable-ease-of-programming/badge/?version=latest)](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/?badge=latest)

Credits and thanks go to [Dan Gittik](https://github.com/dan-gittik), this project is part of his amazing course, _Advanced-System-design_.

# the-unbearable-ease-of-programming

This whole project serves the purpose of learning and experimenting with advance system designs.
It does not solve a concrete problem or well define at that, which reduce to platform - when you cannot well define your problem and solution you build a platform (first rule of advance system designs, the second is that we do not talk about fc).
The platform design is meant to be modular, decoupled and robust; hence making it rather simple to modify, remove and add components.
The platform composes of micro processes and each process has a well define role and does one task and one task only (doing this one task well, I allow myself to add).
Let's dive to the story.

## Table Of Contents

1. [Architecture](/brain_computer_interface/README.md#architecture)
2. [Installation](/brain_computer_interface/README.md#installation)
3. [Packages](/brain_computer_interface/README.md#3-Packages)
4. [Frameworks](/brain_computer_interface/README.md#4-frameworks)
4.1. [MessageQueue](/brain_computer_interface/README.md#41-messagequeue)
4.2. [DataBase](/brain_computer_interface/README.md#42-database)
4.3. [Log](/brain_computer_interface/README.md#43-log)
5. [Flexability and SOLIDness](/brain_computer_interface/README.md#5-flexability-and-solidness)
5.1. [Client](/brain_computer_interface/README.md#51-client)
5.1.1. [File Readers and Writers](/brain_computer_interface/README.md#511-file-readers-and-writers)
5.1.2. [Mind File Formats](/brain_computer_interface/README.md#512-mind-file-formats)
5.1.3. [Client-Server Protocol](/brain_computer_interface/README.md#513-client-server-protocol)
5.2. [Parsers](/brain_computer_interface/README.md#52-parsers)
5.3. [MessageQueue](/brain_computer_interface/README.md#53-messagequeue)
5.3.1. [MessageQueue Context Configuration](/brain_computer_interface/README.md#531-messagequeue-context-configuration)
5.3.2. [MessageQueue Driver](/brain_computer_interface/README.md#532-messagequeue-driver)
5.3.3. [MessageQueue Messages](/brain_computer_interface/README.md#533-messagequeue-messages)
5.4. [DataBase](/brain_computer_interface/README.md#54-database)
5.4.1. [DataBase Driver](/brain_computer_interface/README.md#541-database-driver)
5.5. [API](/brain_computer_interface/README.md#55-api)
5.5.1. [API Format](/brain_computer_interface/README.md#551-api-format)
5.5.2. [API URLs](/brain_computer_interface/README.md#552-api-urls)
5.6. [GUI](/brain_computer_interface/README.md#56-gui)
5.6.1. [Bar Charts](/brain_computer_interface/README.md#561-bar-charts)
5.6.2. [Multiline Graphs](/brain_computer_interface/README.md#562-multiline-graphs)
6. [Tests](/brain_computer_interface/README.md#6-tests)
6.1. [Test tools](/brain_computer_interface/README.md#61-test-tools)
6.1.1. [Test Mind File Creator](/brain_computer_interface/README.md#611-test-mind-file-creator)
6.1.2. [Parser Messages Sniffer](/brain_computer_interface/README.md#612-parser-messages-sniffer)
7. [Additional Information](/brain_computer_interface/README.md#7-additional-information)
7.1. [Scripts](/brain_computer_interface/README.md#71-scripts)
7.2. [Docker](/brain_computer_interface/README.md#72-docker)
7.2.1. [Docker startup](/brain_computer_interface/README.md#721-docker-startup)
7.2.2. [How to add new micro-service](/brain_computer_interface/README.md#722-how-to-add-new-micro-service)

# brain-computer-interface

A brain-computer-interface (BCI), a direct communication pathway between the brain's electrical activity and an external device, most commonly a computer or robotic limb; that's what this project is trying to. I know, crazy, but Elon will surly relate.
We assume, or hope, that one day we will have a hardware that connect to our brain. This project is the software layer on top of that supposed hardware.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/).


## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:sahargavriely/the-unbearable-ease-of-programming.git
    ...
    $ cd the-unbearable-ease-of-programming/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brain-computer-interface] $  # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```


## Packages

The package expose several sub-packages which can be run separately on a different machines.
The sub-packages are:

* [`client`](/brain_computer_interface/client/README.md) - uploads mind and thoughts to the server.
* [`server`](/brain_computer_interface/server/README.md) - receives mind and thoughts from clients.
