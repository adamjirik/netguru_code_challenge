# netguru_code_challenge
Code challenge for Netguru: move database

How to run this repo:

1. install `docker` and `docker-compose`:
  `docker`:
  - Windows users: https://runnable.com/docker/install-docker-on-windows-10
  - Linux users: https://runnable.com/docker/install-docker-on-linux
  `docker-compose`:
  https://docs.docker.com/compose/install/
  
2. clone this repo
3. Running locally:
  - change directory to the root folder `cd <root-folder>`
  - run `docker-compose up -d`
  - run `docker-compose exec api createsuperuser` and follow the terminal instructions to create a super user
  - run `docker-compose exec api migrate` to apply the migrations to the database
  
VIEWS

GET /movies/
Returns all movies stored in the database

GET /movies/<id>/
Returns movie with the id given in the url

POST /movies/
request body:
  - `title` - the title of the movie to be added

Fetches data from OMDb API (http://www.omdbapi.com/), saves it to the database and returns information about the movie.

------------

GET /comments/
Returns all comments posted to all movies.

GET /comments/?movie=<id>
Returns all comments posted to the movie with id given in the url

POST /comments/
request body:
  - `movie` - the id of the movie in the database
  
Posts a comment to the movie given in the request body.

GET /top/
Returns all movie ids from the database and gives them a ranking based on the number of comments.

additional url parameters:
  - `?start=<year>` returns top movies starting from the year <year>
  - `?end=<year>` returns top movies ending at the year <year>

example request: `/top/?start=1990&end=1999` returns all top movies made in the years ranging 1990-1999.
