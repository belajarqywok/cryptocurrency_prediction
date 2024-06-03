from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from restful.controllers import cryptocurrency_controller
from restful.schemas import CryptocurrencyPredictionSchema

# Route
route = APIRouter()

# Controller
__CONTROLLER = cryptocurrency_controller()

# Cryptocurrency Prediction
@route.post(path = '/prediction', tags = ['machine_learning'])
async def cryptocurrency_pred_route(
    payload: CryptocurrencyPredictionSchema = Body(...)
) -> JSONResponse:
    # Cryptocurrency Controller
    return __CONTROLLER.prediction(payload = payload)

