from AlgorithmImports import *
from datetime import datetime
import os
import json

class StockDailyData(PythonData):
    def GetSource(self, config, date, is_live_mode):
        # Construct the absolute path to the JSON file for the given date
        file_name = f"C:/Users/imshii/Documents/Quant/MACD/custom_data/{date.strftime('%Y%m%d')}.json"
        # Return the SubscriptionDataSource pointing to the file
        return SubscriptionDataSource(file_name, SubscriptionTransportMedium.LocalFile)

    def Reader(self, config, line, date, is_live_mode):
        try:
            # Check if the file exists before trying to load it
            file_path = f"C:/Users/imshii/Documents/Quant/MACD/custom_data/{date.strftime('%Y%m%d')}.json"
            if not os.path.exists(file_path):
                Log(f"No data file for {date.strftime('%Y-%m-%d')}. Skipping...")
                return None  # Return None to indicate no data for this date
            
            # Read and parse the file content
            with open(file_path, "r") as file:
                json_data = json.load(file)  # Parse the JSON content
            
            # Populate the StockDailyData instance
            data = StockDailyData()
            data.Symbol = config.Symbol
            data.Time = datetime.strptime(json_data["date"], "%Y-%m-%d")
            data.Value = json_data["close"]  # Set the primary value as the close price
            data["Open"] = json_data["open"]
            data["High"] = json_data["high"]
            data["Low"] = json_data["low"]
            data["Close"] = json_data["close"]
            data["Volume"] = json_data["volume"]
            
            return data
        except Exception as e:
            Log(f"Error reading custom data: {e}")
            return None  # Return None on error
