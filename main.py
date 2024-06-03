import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from restful.routes import route

REST = FastAPI(
    title = "Cryptocurency Prediction Service",
    version = "1.0"
)

# CORS Middleware
REST.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True,
)

REST.include_router(
    router = route,
    prefix = '/crypto'
)