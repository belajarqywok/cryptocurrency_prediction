import os
import json
import numpy as np
import pandas as pd
import onnxruntime as ort
from numpy import append, expand_dims
from decimal import Decimal, ROUND_DOWN
from pandas import read_csv, to_datetime, Timedelta

class Utilities:
    def __init__(self) -> None:
        self.model_path = './models'
        self.posttrained_path = './indonesia_stocks/modeling_datas'
        self.scaler_path = './indonesia_stocks/min_max'

    # def truncate_2_decimal(self, val: float):
    #     return float(Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_DOWN))
    def truncate_2_decimal(self, val: float):
        try:
            return float(Decimal(str(float(val))).quantize(Decimal('0.001'), rounding=ROUND_DOWN))
        except Exception as e:
            print("Decimal error:", e)
            return float(val)


    def denormalization(self, data, min_value, max_value):
        return (data * (max_value - min_value)) + min_value

    async def cryptocurrency_prediction_utils(self,
        days: int, sequence_length: int, model_name: str) -> tuple:

        model_path = os.path.join(self.model_path, f'{model_name}.onnx')
        # session = ort.InferenceSession(model_path)
        try:
            session = ort.InferenceSession(model_path)
        except Exception as e:
            print("ONNX model load error:", e)
            return [], []
        input_name = session.get_inputs()[0].name

        dataframe_path = os.path.join(self.posttrained_path, f'{model_name}.csv')
        dataframe = read_csv(dataframe_path, index_col='Date', parse_dates=True)

        scaler_path = os.path.join(self.scaler_path, f'{model_name}.json')
        with open(scaler_path, 'r') as f:
            scalers = json.load(f)

        min_close = scalers['min_value']['Close']
        max_close = scalers['max_value']['Close']

        lst_seq = dataframe[-sequence_length:].values
        lst_seq = expand_dims(lst_seq, axis=0)

        predicted_prices = {}
        last_date = to_datetime(dataframe.index[-1])

        # for _ in range(days):
        #     predicted = session.run(None, {input_name: lst_seq.astype(np.float32)})[0]

        #     denorm_price = self.denormalization(predicted[0][0], min_close, max_close)

        #     last_date += Timedelta(days=1)
        #     predicted_prices[last_date] = denorm_price.flatten()[0]

        #     lst_seq = np.roll(lst_seq, shift=-1, axis=1)
        #     lst_seq[:, -1, -1] = predicted[0][0][0]


        
        # for _ in range(days):
        #     predicted = session.run(None, {input_name: lst_seq.astype(np.float32)})[0]
        
        #     value = np.array(predicted).flatten()[0]
        #     denorm_price = (value * (max_close - min_close)) + min_close
        
        #     # last_date += pd.Timedelta(days=1)
        #     last_date = pd.to_datetime(last_date) + pd.Timedelta(days=1)
        #     # predicted_prices[last_date.strftime('%Y-%m-%d')] = float(denorm_price)
        #     predicted_prices[last_date] = self.truncate_2_decimal(denorm_price)
        
        #     lst_seq = np.roll(lst_seq, shift=-1, axis=1)
        #     lst_seq[:, -1, -1] = value
        
        for _ in range(days):
            predicted = session.run(None, {input_name: lst_seq.astype(np.float32)})[0]
            value = np.array(predicted).flatten()[0]
            if np.isnan(value):
                continue
            denorm_price = self.denormalization(value, min_close, max_close)
            if np.isnan(denorm_price):
                continue
            last_date = pd.to_datetime(last_date) + pd.Timedelta(days=1)
            predicted_prices[last_date] = self.truncate_2_decimal(denorm_price)
            lst_seq = np.roll(lst_seq, shift=-1, axis=1)
            lst_seq[:, -1, -1] = value

            

        # predictions = [
        #     {'date': date.strftime('%Y-%m-%d'), 'price': float(price)}
        #     for date, price in predicted_prices.items()
        # ]
        predictions = [
            {'date': date.strftime('%Y-%m-%d'), 'price': price}
            for date, price in predicted_prices.items()
        ]

        df_date = dataframe.index[-sequence_length:]
        close_values = dataframe.iloc[-sequence_length:]['Close'].values
        close_denorm = self.denormalization(close_values, min_close, max_close)

        actuals = [
            {'date': to_datetime(date).strftime('%Y-%m-%d'), 'price': self.truncate_2_decimal(price)}
            for date, price in zip(df_date, close_denorm)
        ]

        os.system(f'ls -al {self.model_path}')
        os.system(f'ls -al {self.posttrained_path}')
        os.system(f'ls -al {self.scaler_path}')

        return actuals, predictions
