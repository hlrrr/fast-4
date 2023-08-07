from enum   import StrEnum, auto

from fastapi import FastAPI
from fastapi.middleware.cors    import CORSMiddleware
from h11 import Request

from redis_om   import get_redis_connection, HashModel

from pydantic   import BaseModel

from faker  import Faker

from env    import Environment as env

fkr=Faker()

# fastapi config 
app_payment = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": 0},    # shrink 'Schemas' section
                        )       


origins = [""]
app_payment.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


# redis connection 
redis = get_redis_connection(host=env.redis_02_host,
                             port=env.redis_02_port,
                             decode_responses=True)


# redis models
class Status(StrEnum):
    PENDING = auto()
    COMPLETED = auto()
    CANCELED = auto()
    REFUNDED = auto()

class Order(HashModel):
    ''' redis model for product'''
    product_id:str
    price:float
    quantity:int
    fee:float
    total:float
    status:Status

    class Meta:
        database = redis

# pydantic schemas
class Sch_Order(BaseModel):
    ''' pydantic schema for product '''
    product_id:str
    price:float
    quantity:int
    tax:float
    total:float
    status:Status


# endpoints
@app_payment.post(path='/order',
                  tags=["Order"])
async def creat( product_id:str='01H72D5KH06D74951P2W0E2JW1'):
# async def creat(request=Request,
#                 product_id:str='01H72D5KH06D74951P2W0E2JW1'):
    # body= request.json()
    req = Request.(f'http://locahost:8000/product/{product_id}')
    print(req)
    return
# async def create(produc_id:str, qauntity:int):
#     ''' place an order '''
#     req =   Request()

    


# @app_payment.get(path="/",
#          summary='',)
# async def read_main():
#     ''' intro '''
#     return {"msg": "micro service study",
#             "server": "Payment"}


# @app_payment.get(path='/products')
# def retreive():
#     ''' get all products '''
#     return [Product.get(pk) for pk in Product.all_pks()]


# @app_payment.get(path='/product/{pk}')
# def retrieve(pk:str):
#     ''' get a product '''
#     return Product.get(pk)


# @app_payment.delete(path='/prodcut/{pk}')
# def delete(pk:str):
#     ''' remove a prodcut '''
#     return Product.delete(pk)



# @app_payment.post(path='/dummies')
# def create_random(num:int):
#     ''' add dummy products '''
#     def maker():
#         random_product = Product_sch(name=fkr.pystr_format(),
#                                      price=fkr.pyfloat(min_value=100,
#                                                        max_value=900,
#                                                        right_digits=2),
#                                      quantity=fkr.pyint(max_value=100))
#         data = random_product.model_dump()
#         return Product(**data).save()
#     return [maker() for _ in range(num)]
    