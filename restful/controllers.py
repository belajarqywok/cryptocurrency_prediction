from http import HTTPStatus
from fastapi.responses import JSONResponse
from restful.services import cryptocurrency_svc
from restful.schemas import CryptocurrencyPredictionSchema


# Cryptocurrency Controller
class cryptocurrency_controller:
    # Cryptocurrency Service
    __SERVICE = cryptocurrency_svc()

    # Cryptocurrency Controller
    def prediction(self, payload: CryptocurrencyPredictionSchema) -> JSONResponse:
        try: 
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