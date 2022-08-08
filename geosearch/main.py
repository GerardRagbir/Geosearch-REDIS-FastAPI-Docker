import certifi
import redis
import os
import uvicorn
from redis.commands.json.path import Path
from redis.commands.search.indexDefinition import IndexDefinition
from redis.commands.search.field import GeoField, TextField
from redis.commands.search.query import Query, GeoFilter
from fastapi import FastAPI


# Get Environment Variables
HOST_ID = os.environ.get("HOST_ID")
HOST_PORT = int(os.environ.get("HOST_PORT"))
HEALTH_CHECK_INTERVAL = 60  # in seconds


# Index Creation
index_def = IndexDefinition(prefix=["py_doc:"])


# Define Schema
data_model = (TextField("title"), TextField("type"), GeoField("location"))


# Connect to redis database
redisClient = redis.Redis(
    host='{}.cache.amazonaws.com'.format(HOST_ID),
    port=HOST_PORT,
    ssl_ca_certs=certifi.where(),
    db=0,
    ssl=True,
    health_check_interval=HEALTH_CHECK_INTERVAL
)


'''
# Use redis-sentinel to discover a master node and it's slave network addresses.

sentinel = Sentinel([('localhost', 26379)],
                    ssl=True,
                    ssl_ca_certs='/etc/ssl/certs/ca-certificates.crt')
sentinel.discover_master('redis_master')
'''


fts_client = redisClient.ft("sample")
fts_client.create_index(data_model, definition=index_def)


# Initialize FastAPI
app = FastAPI()

'''
Obligatory Hello World Root
'''
@app.get("/")
async def root():
    return {"message": "Hello World"}


'''
Use /search/{name} to find nearby locations.
Accepts name:string and returns a paginated JSON collection of 10 items.
'''
@app.get("/search/{name}")
async def search_by_name(name: str):
    result = fts_client.search(Query({name}).paging(0,10)).docs
    return result


'''
Use /search/{name}/{distance in KM} to find nearby locations.
Accepts name:string and distance:int and returns a JSON collection.
'''
@app.get("/search/{name}/{distance}")
async def search_nearby(name:str, distance:int):
    nearby_results = fts_client.search(Query("*").add_filter(GeoFilter(name, radius=distance))).docs
    return nearby_results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)