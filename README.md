# Data Compliance Ninja


This is a README file for the DDCNA project.

## Prerequisites

[![Django](https://img.shields.io/badge/Django-3.x-brightgreen.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-5.x-green.svg)](https://www.mongodb.com/)

## Setup Instructions

1.  Clone the repository:

git clone https://github.com/hashptl/server.git


2.  Create a virtual environment:

python3 -m venv env


3.  Activate the virtual environment:

-   For Windows:

        .\env\Scripts\activate

-   For Unix/Linux:

        source env/bin/activate

4.  Install project dependencies:

pip install -r requirements.txt


5.  Set up MongoDB:

-   Create a MongoDB database with the required credentials (username
    and password).

6.  Configure the Django settings:

-   Open the `settings.py` file in the `server` folder.
-   Update the MongoDB database credentials in the `DATABASES` section.

7.  Run database migrations:

python manage.py migrate


8.  Create a superuser for the admin site:

python manage.py createsuperuser


9.  Start the Django development server:

python manage.py runserver

The server should now be running at `http://localhost:8000/`.

## Accessing the Admin Site

To access the admin site, follow these steps:

1.  Open your web browser and go to `http://localhost:8000/admin/`.
2.  Enter your admin username and password.

-   Username: hiren
-   Password: Hiren@1234

You should now have access to the Django admin site.




