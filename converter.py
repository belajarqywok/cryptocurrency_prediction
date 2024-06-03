import json

"""

    Data Mining Assignment - Group 5

"""

class JSONProcessor:
    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file:  str = input_file
        self.output_file: str = output_file
        self.data = None

    def load_json(self) -> None:
        with open(self.input_file, 'r') as file:
            self.data = json.load(file)

    def extract_symbols(self) -> list:
        if self.data is None:
            raise ValueError("data not loaded. call load_json() first.")
        quotes = self.data['finance']['result'][0]['quotes']
        return [quote['symbol'] for quote in quotes]

    def save_json(self, data: list) -> None:
        with open(self.output_file, 'w') as file:
            json.dump({'symbols': data}, file, indent = 4)
            print(f'saved: {self.output_file}')

def main():
    input_file  = './postman/response.json'
    output_file = './postman/symbols.json'
    
    processor = JSONProcessor(input_file, output_file)
    processor.load_json()
    symbols = processor.extract_symbols()
    processor.save_json(symbols)


if __name__ == "__main__": main()
