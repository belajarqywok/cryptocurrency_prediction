from fastapi import FastAPI
from restful.routes import route
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "Cryptocurency Prediction Service",
    version = "1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True,
)

app.include_router(
    router = route,
    prefix = '/crypto',
    tags = ['Crypto']
)

@app.get("/", tags = ['Main'])
def root():
    return RedirectResponse(url="/docs")
