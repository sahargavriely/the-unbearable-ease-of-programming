[![github-workflow](https://github.com/sahargavriely/the-unbearable-ease-of-programming/actions/workflows/github-action.yml/badge.svg)](https://github.com/sahargavriely/the-unbearable-ease-of-programming/actions/workflows/github-action.yml)
[![codecov](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming/graph/badge.svg?token=W0V7MR7T8S)](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming)
[![readthedocs](https://readthedocs.org/projects/the-unbearable-ease-of-programming/badge/?version=latest)](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/?badge=latest)

Credits and thanks go to [Dan Gittik](https://github.com/dan-gittik), this project is part of his amazing course, _Advanced-System-design_.

# the-unbearable-ease-of-programming

This whole project serves the purpose of learning and experimenting with advanced system design.
It does not solve a concrete problem nor the problem is well define, which reduce to a platform - when you cannot well define your problem and solution, you build a platform (first rule of advanced system design, the second is that we do not talk about fc) rather than build a specific solution.
The platform design is meant to be modular, decoupled and robust; hence making the system rather flexible, simple to modify, remove and add components.
The platform composes of micro processes, each process has a well define role and does one task and one task only (doing this one task well, I allow myself to add).
Let's dive to the story.


# brain-computer-interface

A brain-computer-interface (BCI) is a direct communication pathway between the brain's electrical activity and an external device, most commonly a computer or robotic limb; that's what this project is trying to. I know, crazy, but Elon will surly relate.
We assume, or hope, that one day we will have a hardware that connect to our brain. This project is the software layer on top of that supposed hardware.

![flow](https://github.com/sahargavriely/the-unbearable-ease-of-programming/assets/63425950/85c9248d-7cd4-47cf-988c-255f33eccdfc)

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
      $ source venv/bin/activate
      [brain-computer-interface] $  # you're good to go!
      ```

3. To check that everything is working as expected, run the tests: (optional but recommended)

      ```sh
      $ pytest tests/
      ...
      ```

## Packages

The package expose several sub-packages which can be run separately on a different machines.
The sub-packages are:

- [`client`](/brain_computer_interface/client/README.md) - uploads mind to the server.
- [`server`](/brain_computer_interface/server/README.md) - receives minds from clients and forwarding them to the distributer.
- [`distributer`](/brain_computer_interface/distributer/README.md) - distribute information to the different system components.
- [`parser`](/brain_computer_interface/parser/README.md) - listen to raw minds parse them and forwarding them to the distributer.
- [`saver`](/brain_computer_interface/saver/README.md) - listen to parsed minds and forwarding them to the database.
- [`database`](/brain_computer_interface/database/README.md) - holds the system data.
- [`rest`](/brain_computer_interface/rest/README.md) - provides restful api - http request and cli to get the data from the database.
