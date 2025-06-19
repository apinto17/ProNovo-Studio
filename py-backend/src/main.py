from fastapi import FastAPI
from routes.home.route import home_router

app = FastAPI()


app.include_router(home_router)