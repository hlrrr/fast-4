import httpx, time

from enum   import StrEnum, auto

from fastapi import FastAPI
from fastapi.middleware.cors    import CORSMiddleware
from fastapi.background     import BackgroundTasks

from redis_om   import get_redis_connection, HashModel

from pydantic   import BaseModel, Field

from faker  import Faker

from env    import Environment as env

fkr=Faker()

# fastapi config #
app_payment = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": 0},    # shrink 'Schemas' section
                        )       


origins = [""]
app_payment.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


# redis connection #
redis = get_redis_connection(host=env.redis_02_host,
                             port=env.redis_02_port,
                             decode_responses=True)


# redis models #

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
    status:Status = Status.PENDING
    
    class Meta:
        database = redis


# schemas for validation #

class Sch_Order(BaseModel):
    product_id:str = Field(default='01H72D5KEP7AXTJSD4PF2DP6VR')
    quantity:int  = Field(default=1)
    fee_rate:float = Field(default=0.2, repr=False)

    # def __init__(self,**kwargs):
    #     super().__init__(**kwargs)
    #     self.fee:float = kwargs['price']*kwargs['fee_rate']
    #     self.total:float = self.fee + kwargs['price']*kwargs['quantity']
    
    # class Config:
        # orm_mode = True
        # fields = {'fee_rate': {'exclude': True}}


# endpoints #

@app_payment.post(path='/order',
                  tags=["Order"],
                #   response_model=Sch_Order,
                #   response_model_exclude={'fee_rate'},
                  )
async def order_request(request:Sch_Order,
                         background:BackgroundTasks):
    '''place an order'''
    body =  request.model_dump()

    # product =  httpx.get(f'http://127.0.0.1:8000/inventory/product/{body["product_id"]}').json()  # for synchronous

    async with httpx.AsyncClient() as client:
        product = await client.get(f'http://127.0.0.1:8000/inventory/product/{body["product_id"]}')
        product = product.json()

    order = Order(product_id = product['pk'],
                  price = product['price'],
                  quantity = body['quantity'],
                  fee = body['fee_rate'] * product['price'],
                  total = body['fee_rate'] * product['price'] + product['price'] * body['quantity'],
                  )
    order.save()
    background.add_task(order_completed, order)     # need to replace the func with a legitimate one for actual service 
    return order


def order_completed(order: Order):
    ''' change order status to completed '''
    time.sleep(3)
    order.status = Status.COMPLETED
    order.save()

    for enum in Status:
        redis.xadd(enum, order.dict(), '*')    # for redis streams
        # redis.xadd("canceled", order.dict(), '*')    # for redis streams
        # redis.xadd("refunded", order.dict(), '*')    # for redis streams
        # redis.xadd("pending", order.dict(), '*')    # for redis streams



@app_payment.post(path='/order/simualtor',
                  tags=["Order"])
def simualtor(status:Status):
    return status