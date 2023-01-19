# Agency API


## Introduction

 Agency is an application where team members with different roles can view, modify, add and delete actors and movies within the whole team. Actors have attributes name, age and gender. Movies have attributes title, release date and category. The roles that a team member can have:

1. Casting Assistant
 - Can view actors and movies
2. Casting Director
 - All permissions a Casting Assistant has and…
 - Add or delete an actor from the database
 - Modify actors or movies
3. Executive Producer
 - All permissions a Casting Director has and…
 - Add or delete a movie from the database

## Getting Started
### Pre-requisites and Local Development
1. Developers using this application should have the following on their local machine:
- virtualenv
- SQLAlchemy ORM
- PostgreSQL
- Python3
- Flask-Migrate
You can download and install the dependencies mentioned above using pip as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

2. Initialize and activate a virtual env using:
```
python -m virtualenv env
source env/bin/activate
```
Note in Windows using:
```
python -m virtualenv env
source env/Scripts/activate
```

### Backend
From the backend folder to install packages, run:
```
pip install -r requirements.txt
```

If encounter error while installing psycopg2-binary, run:
```
pip install psycopg2-binary
```

To run the application run the following commands:
```
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

The application is run on http://127.0.0.1:5000/ by default
