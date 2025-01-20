# from AlgorithmImports import *

# class MACDStrategy(QCAlgorithm):
#     def Initialize(self):
#         # Set the start and end date for backtesting
#         self.SetStartDate(2020, 1, 1)
#         self.SetEndDate(2023, 1, 1)
        
#         # Set the initial cash for the algorithm
#         self.SetCash(100000)
        
#         # Add the stock for analysis
#         self.symbol = self.AddEquity("AAPL", Resolution.Daily).Symbol
        
#         # Create the MACD indicator with fast period, slow period, and signal period
#         self.macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily)
        
#         # Schedule event to plot the MACD and Signal line
#         self.Schedule.On(self.DateRules.EveryDay(self.symbol),
#                          self.TimeRules.AfterMarketOpen(self.symbol, 5),
#                          self.PlotMACD)
                         
#         # Track if we are invested
#         self.is_invested = False

#     def OnData(self, data):
#         # Ensure MACD is ready before using it
#         if not self.macd.IsReady:
#             return

#         # Check for buy signal
#         if not self.is_invested and self.macd.Current.Value > self.macd.Signal.Current.Value:
#             self.SetHoldings(self.symbol, 1)  # Invest 100% of portfolio
#             self.is_invested = True
#             self.Debug(f"BUY at {data[self.symbol].Close}")

#         # Check for sell signal
#         elif self.is_invested and self.macd.Current.Value < self.macd.Signal.Current.Value:
#             self.Liquidate(self.symbol)
#             self.is_invested = False
#             self.Debug(f"SELL at {data[self.symbol].Close}")

#     def PlotMACD(self):
#         # Plot MACD and Signal values in the charts
#         self.Plot("MACD", "MACD Line", self.macd.Current.Value)
#         self.Plot("MACD", "Signal Line", self.macd.Signal.Current.Value)

from AlgorithmImports import *
from data import StockDailyData
from datetime import datetime, timedelta
import os

class DescendingCustomDataObjectStoreRegressionAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(1990, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)

        # Add custom data
        self.custom_symbol = self.AddData(SortCustomData, "SortCustomData", Resolution.Daily).Symbol
        self.Debug(f"Custom symbol added: {self.custom_symbol}")

        self.received_data = []

    def OnData(self, slice):
        if slice.ContainsKey(self.custom_symbol):
            custom_data = slice[self.custom_symbol]
            self.Debug(f"Time: {custom_data.Time}, Close: {custom_data['Close']}")

            # Ensure data fields are valid
            if custom_data["Open"] == 0 or custom_data["High"] == 0 or custom_data["Low"] == 0 or custom_data["Close"] == 0:
                raise Exception("One or more custom data fields are zero.")

            self.received_data.append(custom_data)

    def OnEndOfAlgorithm(self):
        if not self.received_data:
            raise Exception("No custom data was received during the backtest.")
        self.Debug(f"Custom data received: {len(self.received_data)} entries.")

class SortCustomData(PythonData):
    def get_source(self, config, date, is_live):
        # Use the absolute path to the CSV file
        file_path = os.path.join(Globals.DataFolder, "final_data.csv")
        return SubscriptionDataSource(file_path, SubscriptionTransportMedium.LocalFile, FileFormat.CSV)

    def reader(self, config, line, date, is_live):
        if not line.strip():  # Skip empty lines
            return None
        
        # Split CSV line into columns
        try:
            data = line.split(',')
            if len(data) < 5:  # Ensure the line has enough columns
                raise ValueError(f"Malformed line: {line}")
            
            # Parse the CSV data
            obj_data = SortCustomData()
            obj_data.symbol = config.Symbol
            obj_data.time = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')  # Parse time
            obj_data.value = float(data[4])  # Set close price as the primary value
            obj_data["Open"] = float(data[1])
            obj_data["High"] = float(data[2])
            obj_data["Low"] = float(data[3])
            obj_data["Close"] = float(data[4])
            return obj_data

        except Exception as e:
            Log(f"Error reading custom data: {e}")
            return None
