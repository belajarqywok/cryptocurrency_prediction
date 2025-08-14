import os
from http import HTTPStatus
from fastapi.responses import JSONResponse
from restful.services import cryptocurrency_svc
from restful.schemas import CryptocurrencyPredictionSchema


# Cryptocurrency Controller
class cryptocurrency_controller:
    # Cryptocurrency Service
    __SERVICE = cryptocurrency_svc()

    # Cryptocurrency List
    async def crypto_list(self) -> JSONResponse:
        try:
            DATASETS_PATH = './models'
            DATASETS = sorted(
                [
                    item.replace(".onnx", "") for item in os.listdir(DATASETS_PATH)
                    if os.path.isfile(os.path.join(DATASETS_PATH, item)) and item.endswith('.onnx')
                ]
            )

            return JSONResponse(
                content = {
                    'message': 'Success',
                    'status_code': HTTPStatus.OK,
                    'data': DATASETS
                },
                status_code = HTTPStatus.OK
            )

        except Exception as error_message:
            print(error_message)
            return JSONResponse(
                content = {
                    'message': 'Internal Server Error',
                    'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
                    'data': None
                },
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            )

    # Cryptocurrency Controller
    async def prediction(self, payload: CryptocurrencyPredictionSchema) -> JSONResponse:
        try:
            DATASETS_PATH = './models'
            DATASETS = sorted(
                [
                    item.replace(".onnx", "") for item in os.listdir(DATASETS_PATH)
                    if os.path.isfile(os.path.join(DATASETS_PATH, item)) and item.endswith('.onnx')
                ]
            )

            # Validation
            if (payload.days > 31) or (payload.days < 1):
                return JSONResponse(
                    content = {
                        'message': 'prediction days cannot be more than a month and cannot be less than 1',
                        'status_code': HTTPStatus.BAD_REQUEST,
                        'data': None
                    },
                    status_code = HTTPStatus.BAD_REQUEST
                )

            if payload.currency not in DATASETS:
                return JSONResponse(
                    content = {
                        'message': f'cryptocurrency {payload.currency} is not available.',
                        'status_code': HTTPStatus.BAD_REQUEST,
                        'data': None
                    },
                    status_code = HTTPStatus.BAD_REQUEST
                )


            prediction: dict = await self.__SERVICE.prediction(payload)

            if not prediction :
                return JSONResponse(
                    content = {
                        'message': 'prediction could not be generated, please try again.',
                        'status_code': HTTPStatus.BAD_REQUEST,
                        'data': None
                    },
                    status_code = HTTPStatus.BAD_REQUEST
                )

            return JSONResponse(
                content = {
                    'message': 'prediction success',
                    'status_code': HTTPStatus.OK,
                    'data': {
						'currency': payload.currency,
						'predictions': prediction
					}
                },
                status_code = HTTPStatus.OK
            )

        except Exception as error_message:
            print(error_message)
            return JSONResponse(
                content = {
                    'message': 'internal server error',
                    'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
                    'data': None
                },
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            )
