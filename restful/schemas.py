from pydantic import BaseModel

class CryptocurrencyPredictionSchema(BaseModel) :
	days: int
	currency: str
	