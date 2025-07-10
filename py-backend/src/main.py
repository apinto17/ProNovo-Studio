from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from routes.home.route import home_router
from routes.messages.send_message import send_message_router
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()


app.include_router(home_router)
app.include_router(send_message_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)


# app.openapi()
# with open("../frontend/sdk/schemas/py_openapi.json", "w+") as f:
#     print(app.openapi_schema, "*************")
#     json.dump(app.openapi_schema, f, indent=2)