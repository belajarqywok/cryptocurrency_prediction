from restful.utilities import Utilities
from restful.schemas import CryptocurrencyPredictionSchema

class cryptocurrency_svc:
	# Prediction Utilities
	__PRED_UTILS = Utilities()

	# Prediction Service
	async def prediction(self, payload: CryptocurrencyPredictionSchema) -> dict:
		days: int     = payload.days
		currency: str = payload.currency

		actuals, predictions = await self.__PRED_UTILS.cryptocurrency_prediction_utils(
			days            = days,
			model_name      = currency,
			sequence_length = 60
		)

		return {'actuals': actuals, 'predictions': predictions}
