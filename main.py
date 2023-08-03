from fastapi import FastAPI
from fastapi.middleware.cors    import CORSMiddleware
 
from redis_om   import get_redis_connection, HashModel

from pydantic   import BaseModel 

from env    import Environment as env

# fastapi config 
app = FastAPI()
origins = [""]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

# redis connection 
redis = get_redis_connection(host=env.redis_host,
                             port=env.redis_port,
                             decode_responses=True)



# endpoints
@app.get(path="/")
async def read_main():
    return {"msg": "redis study"}


