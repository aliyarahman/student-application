Development Setup Instructions:

1) Setup a virtualenv (perhaps named 'studentapp')

2) Clone this repository and change into the root directory

3) Run `pip install -r requirements.txt` to install required dependencies

4) Copy config.py.example to config.py in the same directory, and fill in your environment settings

5) Run `python manage.py db upgrade` to create the database tables.

6) Run `python manage.py runserver` to start the development server.