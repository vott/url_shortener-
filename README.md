# Url Shortener

### Request:
    POST: http://localhost:8000/short/
    body: {
        "url": "https://stackoverflow.com/questions"
    }

### Response
    Status Code: 201
    Response Body: {
        "url": "http://localhost:8000/sht/5945e"
    }


## How does it works?

It generates an UUID for each valid call and saves
the url, UUID in a table

## Setup

Verify that docker is installed and run docker-compose up --build from the project's root folder