from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from restful.controllers import cryptocurrency_controller
from restful.schemas import CryptocurrencyPredictionSchema

# Route
route = APIRouter()

# Controller
__CONTROLLER = cryptocurrency_controller()

# Cryptocurrency List
@route.get(path = '/lists')
async def cryptocurrency_list_route() -> JSONResponse:
    # Cryptocurrency Controller
    return await __CONTROLLER.crypto_list()

# Cryptocurrency Prediction
@route.post(path = '/prediction')
async def cryptocurrency_pred_route(
    payload: CryptocurrencyPredictionSchema = Body(...)
) -> JSONResponse:
    # Cryptocurrency Controller
    return await __CONTROLLER.prediction(payload = payload)

