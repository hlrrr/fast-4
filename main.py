from fastapi import FastAPI, Request
from fastapi.middleware.cors    import CORSMiddleware

from inventory.main     import app_inventory
from payment.main   import app_payment


app_main = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": 0},    # shrink 'Schemas' section
                   servers=[{"url": "/payment/docs",
                             "description": "Payment APIs"},
                             {"url": "/inventory/docs",
                             "description": "Inventory APIs"},])


@app_main.get(path="/",
              summary="check root_path")
def find_root_path(request: Request):
    ''' `check the root path` '''
    return {"message": "micro service study", "root_path": request.scope.get("root_path")}


# sub apps
app_main.mount(path='/inventory',
               app=app_inventory,
               name='Inventory')

app_main.mount(path='/payment',
               app=app_payment,
               name='Payment')
