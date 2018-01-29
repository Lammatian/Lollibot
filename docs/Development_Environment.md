# Development environment

This document documents the steps needed to setup the development environment for the project.

### Virtual environment
It is recommended to create and use a python3virtual environment in env/ directory.

To create a virtual environment, run `python3 -m venv env`, to activate it,
run `source env/bin/activate`.

### Installing dependencies

The pip packages required for the application to work are listed in requirements.txt file.
Run `make` to install the dependencies on your machine, or, if you do not have `make` installed,
run `pip install -r requirements.txt`.

This project is what is going to be running on EV3 Brick, so the pip packages in requirements.txt file
have to also work on it.