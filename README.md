# GEO-SEARCH

A basic FastAPI service which performs lookup on a Redis database. There are 2 endpoints usable (3 if you count the obligatory "Hello World").

There is also a basic Dockerfile to host on Docker if needed.

/search/{LOCATION NAME} -> returns a paginated list of similar names to the one you entered

/search/{LOCATION NAME}/{DISTANCE} -> returns a list of nearby locations (near to the LOCATION NAME) within a defined radius as speficied by DISTANCE (in KM).

<h3>TODOs:</h3>

[0] - POST to the database
[0] - Advanced Search Functions
