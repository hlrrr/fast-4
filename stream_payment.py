import time
from env  import Environment as env
from redis_om   import get_redis_connection

from inventory.main import Product

server = get_redis_connection(host=env.redis_02_host,
                                port=env.redis_02_port,
                                decode_responses=True)

def consumer(redis):
    key = 'order_completed'
    group = 'inventory_group'
    
    try:
        redis.xgroup_create(key, group)
    except:
        print('group alredy exists')

    while True:
        try:
            results = redis.xreadgroup(group, key, {key: '>'}, None)

            if results != []:
                for result in results:
                    obj = result[1][0][1]
                    product =  Product.get(obj['product_id'])
                    print("before",product)
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                    print("after",product)
                  
        except Exception as e:
            print('====',str(e))

        time.sleep(1)

if __name__ == "__main__":
    consumer(server)