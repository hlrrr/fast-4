from fastapi import FastAPI
from fastapi.middleware.cors    import CORSMiddleware

from redis_om   import get_redis_connection, HashModel

from pydantic   import BaseModel

from faker  import Faker

from env    import Environment as env

fkr=Faker()

# fastapi config 
app_inventory = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": 0},    # shrink 'Schemas' section
              )       


origins = [""]
app_inventory.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

# redis connection 
redis = get_redis_connection(host=env.redis_01_host,
                             port=env.redis_01_port,
                             decode_responses=True)


# redis models
class Product(HashModel):
    ''' redis model for product'''
    name:str
    price:float
    quantity:int 

    class Meta:
        database = redis

# pydantic schemas
class Sch_Product(BaseModel):
    ''' pydantic schema for product '''
    name:str
    price:float
    quantity:int 


# endpoints 
@app_inventory.get(path="/",
         summary='',)
async def read_main():
    ''' intro '''
    return {"msg": "micro service study",
            "server": "Inventory"}


@app_inventory.get(path='/products/all')
def retreive_all():
    ''' get all products '''
    return [Product.get(pk) for pk in Product.all_pks()]


@app_inventory.get(path='/product/{pk}')
def retrieve_one(pk:str):
    ''' get a product '''
    return Product.get(pk)


@app_inventory.delete(path='/prodcut/{pk}')
def delete(pk:str):
    ''' remove a prodcut '''
    return Product.delete(pk)


@app_inventory.post(path='/product')
def create(product:Sch_Product):
    ''' add a product '''
    data = product.model_dump()
    result = Product(**data).save()
    return result


@app_inventory.post(path='/dummies')
def create_random(num:int):
    ''' add dummy products '''
    def maker():
        random_product = Sch_Product(name=fkr.pystr_format(),
                                     price=fkr.pyfloat(min_value=100,
                                                       max_value=900,
                                                       right_digits=2),
                                     quantity=fkr.pyint(max_value=100))
        data = random_product.model_dump()
        return Product(**data).save()
    return [maker() for _ in range(num)]
    