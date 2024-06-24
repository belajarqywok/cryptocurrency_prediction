import os
from joblib import load
from numpy import append, expand_dims
from pandas import read_json, to_datetime, Timedelta

from tensorflow.keras.models import load_model


class Utilities:
	def __init__(self) -> None:
		self.model_path = './models'
		self.posttrained_path = './posttrained'
		self.scaler_path = './pickles'

	async def cryptocurrency_prediction_utils(self,
		days: int, sequence_length: int, model_name: str) -> tuple:
		model_path = os.path.join(self.model_path, f'{model_name}.keras')
		model = load_model(model_path)

		dataframe_path = os.path.join(self.posttrained_path, f'{model_name}-posttrained.json')
		dataframe = read_json(dataframe_path)
		dataframe.set_index('Date', inplace = True)

		minmax_scaler = load(os.path.join(self.scaler_path, f'{model_name}_minmax_scaler.pickle'))
		standard_scaler = load(os.path.join(self.scaler_path, f'{model_name}_standard_scaler.pickle'))

		lst_seq = dataframe[-sequence_length:].values
		lst_seq = expand_dims(lst_seq, axis = 0)

		# Predicted
		predicted_prices = {}
		last_date = to_datetime(dataframe.index[-1])

		for _ in range(days):
			predicted_price = model.predict(lst_seq)
			last_date       = last_date + Timedelta(days = 1)

			predicted_prices[last_date] = minmax_scaler.inverse_transform(predicted_price)
			predicted_prices[last_date] = standard_scaler.inverse_transform(predicted_prices[last_date])

			lst_seq = append(lst_seq[:, 1:, :], [predicted_price], axis = 1)

		predictions = [
			{'date': date.strftime('%Y-%m-%d'), 'price': float(price)} \
				for date, price in predicted_prices.items()
    ]

		# Actual
		df_date = dataframe.index[-sequence_length:].values
		df_date = [to_datetime(date) for date in df_date]

		dataframe[['Close']] = minmax_scaler.inverse_transform(dataframe)
		dataframe[['Close']] = standard_scaler.inverse_transform(dataframe)
		df_close = dataframe.iloc[-sequence_length:]['Close'].values

		actuals = [
			{'date': date.strftime('%Y-%m-%d'), 'price': close} \
				for date, close in zip(df_date, df_close)
		]
        
		return actuals, predictions
