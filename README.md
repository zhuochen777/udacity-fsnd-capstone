# Agency API


## Motivation for this project

 Agency is an application where team members with different roles can view, modify, add and delete actors and movies within the whole team. Actors have attributes name, age and gender. Movies have attributes title, release date and category. The roles that a team member can have are:

1. Casting Assistant
 - Can view actors and movies
2. Casting Director
 - All permissions a Casting Assistant has and…
 - Add or delete an actor from the database
 - Modify actors or movies
3. Executive Producer
 - All permissions a Casting Director has and…
 - Add or delete a movie from the database

## Getting Started Locally
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

2. Initialize and activate a virtual env in the project folder using:
```
python -m virtualenv env
source env/bin/activate
```
Note in Windows using:
```
python -m virtualenv env
source env/Scripts/activate
```

3. From the project folder to install dependencies, run:
```
pip install -r requirements.txt
```

If encounter error while installing psycopg2-binary, run:
```
pip install psycopg2-binary
```

To create a requirement.txt with a list of all the required packages, run:
```
pip freeze > requirements.txt
```

4. In models.py, connect application to your local postgres database, uncomment following and change config based your local environment:
```
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'zhuochen')
DB_NAME = os.getenv('DB_NAME', 'agency')
database_path = 'postgresql://{}@{}/{}'.format(DB_USER, DB_HOST, DB_NAME)
```

Since we do not access Render environment variable, comment out:
```
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)
```

5. Auth0 bearer tokens for different roles are provided in test_app.py. You can use them or generate your own tokens. The steps can be found in Authentication section.

6. To run the application run the following commands in project folder:
```
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

The application is run on http://127.0.0.1:5000/ by default.

7. To execute tests, run:
```
python test_app.py
```

## API Reference
### Getting Started
- Base URL: https://render-deployment-capstone.onrender.com/
- Auth0 Authentication:
1. Go to Auth0 website, sign up an account and log in
2. Create an application called Agency with application type: Regular Web Application
3. Go to Applications, go to Agency Settings, input following:
Token Endpoint Authentication Method: Post,
Allowed Callback URLs: https://render-deployment-capstone.onrender.com
Application Login URI: https://render-deployment-capstone.onrender.com
Allowed Logout URLs: https://render-deployment-capstone.onrender.com
ID Token Expiration: 86400(should be small, set 86400 for test purpose)
4. Go to APIs, click Create API, input following:
Name: AgencyAPI
Identifier: agency
signing algorithm: RS256
5. Go to AgencyAPI, under Permissions add permissions:
get:actors
get:movies
post:actor
post:movie
patch:actor
patch:movie
delete:actor
delete:movie
6. Go to Roles, create three roles and add permissions for each one:
- Casting Assistant, permissions: get:actors, get:movies
- Casting Director, permissions: get:actors, get:movies, patch:actor, patch:movie, post:actor, delete:actor
- Executive Producer, permissions: get:actors, get:movies, patch:actor, patch:movie, post:actor, delete:actor, post:movie, delete:movie
7. Go to API-AgencyAPI, in RBAC Settings, turn on 'Enable RBAC' and 'Add Permissions in the Access Token' and save changes
8. Go to Users, create three users and assign role for each one:
- Email: castingassistant1@gmail.com, password: astingassistant1@gmail.com, role: Casting Assistant
- Email: castingdirector1@gmail.com, password: castingdirector1@gmail.com, role: Casting Director
- Email: executiveproducer1@gmail.com, password: executiveproducer1@gmail.com, role: Executive Producer
9. Auth0 application endpoint:
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}} \
Log in end point with credentials of an user to get access token which is after the # part.
10. When you make a API request, include token in headers in the following format and repleace 'token' with token value got in step 9:
-H "Authorization: Bearer {token}"

### Error Handling
Errors are returned in JSON format as following:
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
The API will return four error types when requests fail:
- 401: Invalid token
- 403: Permission not found
- 404: Resource Not Found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal Server Error

### End Points
#### GET /actors
Requires get:actors permission\
Returns the list of all actors\
Sample request:
curl -X GET "https://render-deployment-capstone.onrender.com/actors" -H "Authorization: Bearer {token}"
Sample response:
```
{
    "actors": [
        {
            "age": 30,
            "gender": "female",
            "id": 1,
            "name": "actor1"
        },
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "actor2"
        }
    ],
    "success": true
}
```

#### GET /movies
Requires get:movies permission\
Returns the list of all movies\
Sample request:
curl -X GET "https://render-deployment-capstone.onrender.com/movies" -H "Authorization: Bearer {token}"
Sample response:
```
{
    "movies": [
        {
            "category": "action",
            "id": 1,
            "releasedate": "01012022",
            "title": "test"
        },
        {
            "category": "adventure",
            "id": 2,
            "releasedate": "10102000",
            "title": "test2"
        }
    ],
    "success": true
}
```

#### POST /actors
Requires post:actor permission\
Returns the list of all actors after a new actor is created\
Sample request:
curl -X POST "https://render-deployment-capstone.onrender.com/actors" -H "Authorization: Bearer {token}" -H "Content-Type:application/json" -d '{"name":"actor3", "age":3, "gender":"male"}'
Sample response:
```
{
    "actors": [
        {
            "age": 30,
            "gender": "female",
            "id": 1,
            "name": "actor1"
        },
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "actor2"
        },
        {
            "age": 3,
            "gender": "male",
            "id": 3,
            "name": "actor3"
        }
    ],
    "success": true
}
```

#### POST /movies
Requires post:movie permission\
Returns the list of all movies after a new movie is created\
Sample request:
curl -X POST "https://render-deployment-capstone.onrender.com/movies" -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"title":"movie_1", "release_date":"02022002", "category":"comedy"}'
Sample response:
```
{
    "movies": [
        {
            "category": "action",
            "id": 1,
            "releasedate": "01012022",
            "title": "test"
        },
        {
            "category": "adventure",
            "id": 2,
            "releasedate": "10102000",
            "title": "test2"
        },
        {
            "category": "adventure",
            "id": 3,
            "releasedate": "10102000",
            "title": "test333"
        },
        {
            "category": "adventure",
            "id": 4,
            "releasedate": "10102000",
            "title": "test333"
        },
        {
            "category": "comedy",
            "id": 5,
            "releasedate": "02022002",
            "title": "movie_1"
        }
    ],
    "success": true
}
```

#### PATCH /movies/<int:movie_id>
Requires patch:movie permission\
Returns the updated movie\
Sample request:
curl -X PATCH "https://render-deployment-capstone.onrender.com/movies/4" -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"title":"movie_4"}'
Sample response:
```
{
    "success": true,
    "updated_movie": [
        {
            "category": "adventure",
            "id": 4,
            "releasedate": "10102000",
            "title": "movie_4"
        }
    ]
}
```

#### PATCH /actors/<int:actor_id>
Requires patch:actor permission\
Returns the updated actor\
Sample request:
curl -X PATCH "https://render-deployment-capstone.onrender.com/actors/1" -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"age":58}'
Sample response:
```
{
    "success": true,
    "updated_actor": [
        {
            "age": 58,
            "gender": "female",
            "id": 1,
            "name": "actor1"
        }
    ]
}
```

#### DELETE /actors/<int:actor_id>
Requires delete:actor permission\
Returns the list of actors after an actor is deleted\
Sample request:
curl -X DELETE "https://render-deployment-capstone.onrender.com/actors/3" -H "Authorization: Bearer {token}"
Sample response:
```
{
    "actors": [
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "actor2"
        },
        {
            "age": 3,
            "gender": "male",
            "id": 4,
            "name": "actor3"
        },
        {
            "age": 58,
            "gender": "female",
            "id": 1,
            "name": "actor1"
        }
    ],
    "delete_actor_id": 3,
    "success": true
}
```

#### DELETE /movies/<int:movie_id>
Requires delete:movie permission\
Returns the list of movies after a movie is deleted\
Sample request:
curl -X DELETE "https://render-deployment-capstone.onrender.com/movies/1" -H "Authorization: Bearer {token}"
Sample response:
```
{
    "delete_movie_id": 1,
    "movies": [
        {
            "category": "adventure",
            "id": 2,
            "releasedate": "10102000",
            "title": "test2"
        },
        {
            "category": "adventure",
            "id": 3,
            "releasedate": "10102000",
            "title": "test333"
        },
        {
            "category": "comedy",
            "id": 5,
            "releasedate": "02022002",
            "title": "movie_1"
        },
        {
            "category": "adventure",
            "id": 4,
            "releasedate": "10102000",
            "title": "movie_4"
        }
    ],
    "success": true
}
```
