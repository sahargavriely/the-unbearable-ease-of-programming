[![github-workflow](https://github.com/sahargavriely/the-unbearable-ease-of-programming/actions/workflows/github-action.yml/badge.svg)](https://github.com/sahargavriely/the-unbearable-ease-of-programming/actions/workflows/github-action.yml)
[![codecov](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming/graph/badge.svg?token=W0V7MR7T8S)](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming)
[![readthedocs](https://readthedocs.org/projects/the-unbearable-ease-of-programming/badge/?version=latest)](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/?badge=latest)

Credits and thanks go to [Dan Gittik](https://github.com/dan-gittik), this project is part of his amazing course, _Advanced-System-design_.

# the-unbearable-ease-of-programming

This whole project serves the purpose of learning and experimenting with advanced system design.
The learning you can find at the [code-of-conduct](/CODE_OF_CONDUCT.md) file, in a succinct way; in many ways this is the golden gem of the project, it is about how to design rather than just having a good design; it is the abstraction while anything else is the implementation.
The experimenting part is the [brain-computer-interface](/brain_computer_interface/) python package and anything around it. It is a good (very good) example of a good design, it does not solve a concrete problem nor the problem is well define, which reduce to a platform - when you cannot well define your problem and solution, you build a platform (first rule of advanced system design, the second is that we do not talk about fc) rather than build a specific solution.
The platform design is meant to be modular, decoupled and robust; hence making the system rather flexible, simple to modify, remove and add components.
The platform composes of micro processes, each process has a well define role and does one task and one task only (doing this one task well, I allow myself to add).
Note, the the project was being written in steps, at the beginning I did not know how everything is suppose to work and so I developed accordingly, later on I had more concrete knowledge but it was never complete; resulting in the platform you can see here.
Let's go over the background.


# brain-computer-interface

A brain-computer-interface (BCI) is a direct communication pathway between the brain's electrical activity and an external device, most commonly a computer or robotic limb.
The project is assuming BCI hardware and is a software layer that commune with it, handle the data the hardware provides, parses it, saves it, publishes it and exposes it (Elon, if you want to collaborate let me know).
It is build in such way that allows easy modification, deletion and addition - addition of more of the same and addition of new components completely.

![flow](https://github.com/sahargavriely/the-unbearable-ease-of-programming/assets/63425950/85c9248d-7cd4-47cf-988c-255f33eccdfc)

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

      ```sh
      $ git clone git@github.com:sahargavriely/the-unbearable-ease-of-programming.git
      ...
      $ cd the-unbearable-ease-of-programming/
      ```

2. Run the installation script and activate the virtual environment (if you don't care about testing it and you're going to use docker consider jumping clause 4):

      ```sh
      $ ./scripts/install.sh
      ...
      $ source venv/bin/activate
      [brain-computer-interface] $  # you're good to go!
      ```

3. To check that everything is working as expected, run the tests: (optional but recommended)

      ```sh
      $ pytest tests/
      ...
      ```

4. Run the packages
    1. All of them at once with docker compose:

        ```sh
        $ ./scripts/run_pipeline.sh
        ...
        ```

    2. Selectively, run the packages one by one, choose which package to run. To do so you should go over each package's documentation and view how to run it. you can also run it in a docker environment with the `build_and_run_dockerfile.sh` in the scripts directory (based on `Docker.base` file), and in the docker environment run the same command you would have used without the docker (again, you can find the specific command in the specific documentation).

## Packages

The package expose several sub-packages which can be run separately on a different machines.
The sub-packages are:

- [`client`](/brain_computer_interface/client/README.md) - uploads mind to the server.
- [`server`](/brain_computer_interface/server/README.md) - receives minds from clients and forwarding them to the distributer.
- [`distributer`](/brain_computer_interface/distributer/README.md) - distribute information to the different system component (driver-based).
- [`parser`](/brain_computer_interface/parser/README.md) - listen to raw minds, parse them and forwards them back to the distributer.
- [`saver`](/brain_computer_interface/saver/README.md) - listens to parses minds and saves them to the database.
- [`database`](/brain_computer_interface/database/README.md) - holds the system data (driver-based).
- [`rest`](/brain_computer_interface/rest/README.md) - provides restful api - http request and cli to get the data from the database.
