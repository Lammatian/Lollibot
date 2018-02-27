# Development environment

This document documents the steps needed to setup the development environment for the project.

### Virtual environment
It is recommended to create and use a python3virtual environment in env/ directory.

To create a virtual environment, run `python3 -m venv env`, to activate it,
run `source env/bin/activate`.

On the EV3 brick, the python version currently installed is Python 3.4. The latest stable Python 3 is 3.6, which is worthy of note because there were a few syntax changes since 3.4. If you're used to 3.5+ (eg: function and variable annotation, the new async syntax, ...), bear in mind we should probably try to target Python 3.4.

The default version of Python 3 on dice is 3.4 (but other versions are available).

### Installing dependencies

The pip packages required for the application to work are listed in requirements.txt file.
Run `make` to install the dependencies on your machine, or, if you do not have `make` installed,
run `pip install -r requirements.txt`.

This project is what is going to be running on EV3 Brick, so the pip packages in requirements.txt file
have to also work on it.

### Working on the bot: utility and QoL

I'd recommend adding your SSH key to the robot. You can do this with `ssh-copy-id robot@ev3dev`. Then, you can `ssh-add` your key and not have to type in your password every time you `ssh` or `scp`.

#### Watching for file changes and automatically pushing them to the robot

`cd` into the Lollibot repo and run this:

`while inotifywait -e close_write *.py */*.py; do scp -r . robot@ev3dev:/home/robot/; done`

This syncs the git history, too, which is unnecessary, but eh.

(If you want it to be neater, install `rsync` on the robot and use an exclusion list)
