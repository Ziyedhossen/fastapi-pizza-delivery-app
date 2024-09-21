from fastapi import FastAPI
from auth_routes import auth_routes
from order_routes import order_routes
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_routes)
app.include_router(order_routes)

