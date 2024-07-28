import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


"""

    Data Mining Assignment - Group 5

"""


from warnings import filterwarnings
filterwarnings('ignore')

class DataProcessor:
    def __init__(self, datasets_path):
        self.datasets_path = datasets_path
        self.datasets = self._get_datasets()

    def _get_datasets(self):
        return sorted([
            item for item in os.listdir(self.datasets_path)
            if os.path.isfile(os.path.join(self.datasets_path, item)) and item.endswith('.csv')
        ])

    @staticmethod
    def create_sequences(df, sequence_length):
        labels, sequences = [], []
        for i in range(len(df) - sequence_length):
            seq = df.iloc[i:i + sequence_length].values
            label = df.iloc[i + sequence_length].values[0]
            sequences.append(seq)
            labels.append(label)
        return np.array(sequences), np.array(labels)

    @staticmethod
    def preprocess_data(dataframe):
        for col in dataframe.columns:
            if dataframe[col].isnull().any():
                if dataframe[col].dtype == 'object':
                    dataframe[col].fillna(dataframe[col].mode()[0], inplace = True)
                else:
                    dataframe[col].fillna(dataframe[col].mean(), inplace = True)
        return dataframe

    @staticmethod
    def scale_data(dataframe, scaler_cls):
        scaler = scaler_cls()
        dataframe['Close'] = scaler.fit_transform(dataframe[['Close']])
        return scaler, dataframe

class ModelBuilder:
    @staticmethod
    def build_model(input_shape):
        model = Sequential([
            LSTM(units=128, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            Dense(128, activation='relu'),
    
            LSTM(units=64, return_sequences=True),
            Dropout(0.2),
            Dense(64, activation='relu'),
    
            LSTM(units=64, return_sequences=True),
            Dropout(0.2),
            Dense(64, activation='relu'),
    
            LSTM(units=64, return_sequences=False),
            Dropout(0.2),
            Dense(64, activation='relu'),
    
            Dense(32, activation='softmax'),
            Dense(units=1)
        ])
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        return model

class Trainer:
    def __init__(self, model, model_file, sequence_length, epochs, batch_size):
        self.model = model
        self.model_file = model_file
        self.sequence_length = sequence_length
        self.epochs = epochs
        self.batch_size = batch_size

    def train(self, X_train, y_train, X_test, y_test):
        early_stopping = EarlyStopping(monitor = 'val_loss', patience = 5, mode = 'min')

        model_checkpoint = ModelCheckpoint(
          filepath       = self.model_file,
          save_best_only = True,
          monitor        = 'val_loss',
          mode           = 'min'
        )

        history = self.model.fit(
            X_train, y_train,
            epochs          = self.epochs,
            batch_size      = self.batch_size,
            validation_data = (X_test, y_test),
            callbacks       = [early_stopping, model_checkpoint]
        )

        return history

class PostProcessor:
    @staticmethod
    def inverse_transform(scaler, data):
        return scaler.inverse_transform(data)

    @staticmethod
    def save_json(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)

def main():
    datasets_path = './datasets'
    models_path   = './models'
    posttrained   = './posttrained'
    pickle_file   = './pickles'

    sequence_length = 60
    epochs = 200
    batch_size = 32

    data_processor = DataProcessor(datasets_path)

    for dataset in data_processor.datasets:
        print(f"[TRAINING] {dataset.replace('.csv', '')} ")

        dataframe = pd.read_csv(os.path.join(datasets_path, dataset), index_col='Date')[['Close']]
        model_file = os.path.join(models_path, f"{dataset.replace('.csv', '')}.keras")

        # dataframe = data_processor.preprocess_data(dataframe)
        dataframe.dropna(inplace = True)
        standard_scaler, dataframe = data_processor.scale_data(dataframe, StandardScaler)
        minmax_scaler, dataframe = data_processor.scale_data(dataframe, MinMaxScaler)

        sequences, labels = data_processor.create_sequences(dataframe, sequence_length)
        input_shape = (sequences.shape[1], sequences.shape[2])
        model = ModelBuilder.build_model(input_shape)

        train_size = int(len(sequences) * 0.8)
        X_train, X_test = sequences[:train_size], sequences[train_size:]
        y_train, y_test = labels[:train_size], labels[train_size:]

        trainer = Trainer(model, model_file, sequence_length, epochs, batch_size)
        trainer.train(X_train, y_train, X_test, y_test)

        dataframe_json = {'Date': dataframe.index.tolist(), 'Close': dataframe['Close'].tolist()}

        PostProcessor.save_json(
          os.path.join(posttrained, f'{dataset.replace(".csv", "")}-posttrained.json'),
          dataframe_json
        )

        joblib.dump(minmax_scaler, os.path.join(pickle_file, f'{dataset.replace(".csv", "")}_minmax_scaler.pickle'))
        joblib.dump(standard_scaler, os.path.join(pickle_file, f'{dataset.replace(".csv", "")}_standard_scaler.pickle'))

        model.load_weights(model_file)
        model.save(model_file)

        print("\n\n")

if __name__ == "__main__":
    main()
