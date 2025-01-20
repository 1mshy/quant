from AlgorithmImports import *
from datetime import datetime
import json
import os

class StockDailyData(PythonData):
    def GetSource(self, config, date, is_live_mode):
        # Construct the path to the JSON file for the given date
        file_name = f"custom_data/{date.strftime('%Y%m%d')}.json"
        file_path = os.path.join(Globals.DataFolder, file_name)
        return SubscriptionDataSource(file_path, SubscriptionTransportMedium.LocalFile)

    def Reader(self, config, line, date, is_live_mode):
        # Parse the JSON file content
        try:
            # with open("C:/Users/imshii/Documents/Quant/MACD/LocalData.json", "w") as f:
            #     f.write(str(line))
            json_data = json.loads(line)  # The file should have only one JSON object
            data = StockDailyData()
            data.Symbol = config.Symbol
            data.Time = datetime.strptime(json_data["date"], "%Y-%m-%d")
            data.Value = json_data["close"]  # Set the primary value as the close price
            data["Open"] = json_data["open"]
            data["High"] = json_data["high"]
            data["Low"] = json_data["low"]
            data["Close"] = json_data["close"]
            data["Volume"] = json_data["volume"]
            print(f"Read data: {data.Time}, Close: {data.Value}")
            # self.debug(f"Read data: {data.Time}, Close: {data.Value}")
            return data
        except Exception as e:
            # Log(f"Error reading custom data: {e}")
            return None
