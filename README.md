#  Casting Agency Full Stack 

The project is an educational project and the capstone project of udacity full-stack nanodegree program .
it is a demonstration of API development techniques using flask micro-framework and user authentication and authorization using OIDC and jwt and heroku deployment .
most remarakable modules used are SQLAlchemy, flask-cors and jose .
code style in the backend is [PEP8](https://www.python.org/dev/peps/pep-0008/)

## Motivation

- help casting agencies standarize their job
- demonstrate my ability in flask stack
- aquire my nanodegree certificate


## Getting Started


1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)





2. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


3. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Running the server

from the root folder, execute:

```bash
./run.sh
```

This will first add environment vars from install.sh then run the app using gunicorn on port 8080


## Testing locally

from the root folder, execute:

```bash
./test.sh
```

This will first add environment vars from install.sh then test the app using test_app.py

## Testing the hosted API

you can run the `capstone-casting-agency.postman_collection.json` collection from postman

## Authorization
### Authorization way
all endpoints are requiring attaching a bearer token to the `Authorization` header

### Roles And Permissions

- assistant
    - get:movies
    - get:actors
- director
    - all assistant roles +
    - post:actors
    - patch:actors
    - delete:actors
    - patch:movies
- producer
    - all director roles +
    - post:movies
    - delete:movies


## API Reference
### Error Handling
The API will respond with a json response that contains error code and failure message

#### Sample error response
```
{
    "success" : false,
    "error" : 404,
    "message" : "Resource Not Found"
}
```

Expected errors are 422,404,401,403,500,405

### Endpoints

#### GET /actors
- Request Arguments: None
- Returns: Available actors in an object
- Requires: Assistant role 


```json

{
    "actors": {
        "1": {
            "age": 48,
            "gender": "M",
            "id": 1,
            "movies": [
                {
                    "id": 1,
                    "title": "Mafia"
                }
            ],
            "name": "Ahmed El Sakka"
        },
        "2": {
            "age": 51,
            "gender": "M",
            "id": 2,
            "movies": [
                {
                    "id": 1,
                    "title": "Mafia"
                }
            ],
            "name": "Mustafa Sha3ban"
        },
        "3": {
            "age": 44,
            "gender": "F",
            "id": 3,
            "movies": [
                {
                    "id": 1,
                    "title": "Mafia"
                }
            ],
            "name": "Mona Zaki"
        },
        "4": {
            "age": 51,
            "gender": "M",
            "id": 4,
            "movies": [
                {
                    "id": 2,
                    "title": "She turned me into a criminal"
                }
            ],
            "name": "Ahmed Helmy"
        },
        "5": {
            "age": 46,
            "gender": "F",
            "id": 5,
            "movies": [
                {
                    "id": 2,
                    "title": "She turned me into a criminal"
                }
            ],
            "name": "Ghada Adel"
        },
        "6": {
            "age": 43,
            "gender": "F",
            "id": 6,
            "movies": [
                {
                    "id": 2,
                    "title": "She turned me into a criminal"
                }
            ],
            "name": "Reham 3bd el 8afour"
        }
    },
    "status": 200,
    "success": true
}

```

#### GET /movies
- Request Arguments: None
- Returns: Available movies in an object
- Requires: Assistant role 


```json

{
    "movies": {
        "1": {
            "actors": [
                {
                    "id": 1,
                    "name": "Ahmed El Sakka"
                },
                {
                    "id": 2,
                    "name": "Mustafa Sha3ban"
                },
                {
                    "id": 3,
                    "name": "Mona Zaki"
                }
            ],
            "id": 1,
            "release_date": "Sat, 01 Jan 2000 00:00:00 GMT",
            "title": "Mafia"
        },
        "2": {
            "actors": [
                {
                    "id": 4,
                    "name": "Ahmed Helmy"
                },
                {
                    "id": 5,
                    "name": "Ghada Adel"
                },
                {
                    "id": 6,
                    "name": "Reham 3bd el 8afour"
                }
            ],
            "id": 2,
            "release_date": "Wed, 26 Jul 2006 00:00:00 GMT",
            "title": "She turned me into a criminal"
        }
    },
    "status": 200,
    "success": true
}

```


#### POST /actors
- Request Arguments: None
- posts new actor to the database
- payload
    - name : string
    - age : integer
    - gender : char
- Requires director role
- Returns: An object with a single key `created` that contains the posted actor

- sample response :

```json

{
    "created": {
        "age": 44,
        "gender": "M",
        "id": 7,
        "movies": [],
        "name": "Jason Statham"
    },
    "created_at": "Tue, 28 Sep 2021 13:20:14 GMT",
    "status": 200,
    "success": true
}

```

#### PATCH /actors/<int:actor_id>
- Request Arguments: None
- edits the actor with id actor_id and returns 404 if not found
- Returns: An object with a single `actor` that contains the edited actor
- payload
    - name : string
    - age : integer
    - gender : char
- Requires director role


- sample response :

```json

{
    "actor": {
        "age": 45,
        "gender": "M",
        "id": 7,
        "movies": [],
        "name": "Jason S."
    },
    "modified_at": "Tue, 28 Sep 2021 13:26:39 GMT",
    "status": 200,
    "success": true
}

```


#### DELETE /actors/<int:actor_id>

- Deletes the actor with the given actor_id
- Requires director role

- Sample Response

```json

{
    "deleted_id": 7,
    "deleted_at": "Tue, 28 Sep 2021 13:30:36 GMT",
    "status": 200,
    "success": true
}

```

#### POST /movies
- Request Arguments: None
- posts new movie to the database
- payload
    - title : string
    - release_date : string in the format `'%m %d %Y'` , for example : `05 22 2023`
- Requires executive producer role
- Returns: An object with a single key `created` that contains the posted movie

- sample response :

```json

{
    "created": {
        "actors": [],
        "id": 3,
        "release_date": "Mon, 22 May 2023 00:00:00 GMT",
        "title": "to be or not to be"
    },
    "created_at": "Tue, 28 Sep 2021 13:36:42 GMT",
    "status": 200,
    "success": true
}

```

#### PATCH /movies/<int:movie_id>
- Request Arguments: None
- edits the movie with id movie_id and returns 404 if not found
- Returns: An object with a single `movie` that contains the edited movie
- payload
    - title : string
    - release_date : string in the format `'%m %d %Y'` , for example : `06 30 2024`
- Requires director role
- sample response :

```json

{
    "modified_at": "Tue, 28 Sep 2021 13:39:37 GMT",
    "movie": {
        "actors": [],
        "id": 3,
        "release_date": "Sun, 30 Jun 2024 00:00:00 GMT",
        "title": "to be or not to be!"
    },
    "status": 200,
    "success": true
}

```


#### DELETE /movies/<int:movie_id>

- Deletes the movie with the given movie_id
- Requires producer role

- Sample Response

```json

{
    "deleted_at": "Tue, 28 Sep 2021 13:40:54 GMT",
    "deleted_id": 3,
    "status": 200,
    "success": true
}

```

## Deployment

after creating a heroku app, you can add its remote using this command

```bash
heroku git:remote <your app remote>
```

Then you can commit and push changes using those commands

```bash
git add .
git commit -m <message>
git push heroku master
```

This will build and run the app using `Procfile` data

>> The app is hosted at `https://casting-agency-capstone-303.herokuapp.com/`

## Authors
- Mahmoud Khayralla (Me)

## Acknowledgements
- I would like to thank the instructor  for making things very simple to make and giving me very deep knowledge of scurity issues in developing microservices
- I'd like to thank [Udacity](http://udacity.com/) for their great contribution to the IT learning community
- I'd like to thank the [NTL_initiative](http://techleaders.eg/learning-tracks/) for giving me this chance