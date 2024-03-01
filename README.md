# Homework 2
This is a basic demo of a sqlite database with a web interface built with [Flask](https://flask.palletsprojects.com/en/3.0.x/). The interface uses [Pico CSS](https://picocss.com) as well as code from the official [Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/).

## Environment
You must first install Python 3.12, then install Flask (whether to do this in a virtual environment is up to you).

All commands must be run from the root directory of the project (i.e. the directory containing `hw2` and `instance`).

## Set up database
The database is stored at `instance/database.db`. To reset and initialize it with the data given in the instructions for the homework, run `flask --app hw2 init-db`.

## Run
To start the application, run `flask --app hw2 run`. This will output a link that you can open in a web browser.