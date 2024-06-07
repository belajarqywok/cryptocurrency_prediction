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
    def crypto_list(self) -> JSONResponse:
        try:
            DATASETS_PATH = './datasets'
            DATASETS = sorted(
                [
                    item.replace(".csv", "") for item in os.listdir(DATASETS_PATH)
                    if os.path.isfile(os.path.join(DATASETS_PATH, item)) and item.endswith('.csv')
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
    def prediction(self, payload: CryptocurrencyPredictionSchema) -> JSONResponse:
        try:
            # DATASETS_PATH = './datasets'
            # DATASETS = sorted(
            #     [
            #         item.replace(".csv", "") for item in os.listdir(DATASETS_PATH)
            #         if os.path.isfile(os.path.join(DATASETS_PATH, item)) and item.endswith('.csv')
            #     ]
            # )

            # # Model Validation
            # if payload not in DATASETS:
            #     return JSONResponse(
            #         content = {
            #             'message': 'Request Failed 1',
            #             'status_code': HTTPStatus.BAD_REQUEST,
            #             'data': None
            #         },
            #         status_code = HTTPStatus.BAD_REQUEST
            #     )


            prediction: list = self.__SERVICE.prediction(
                payload = payload
            )

            if not prediction :
                return JSONResponse(
                    content = {
                        'message': 'Request Failed',
                        'status_code': HTTPStatus.BAD_REQUEST,
                        'data': None
                    },
                    status_code = HTTPStatus.BAD_REQUEST
                )

            return JSONResponse(
                content = {
                    'message': 'Prediction Success',
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
                    'message': 'Internal Server Error',
                    'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
                    'data': None
                },
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            )