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

class MyStockAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(1990, 12, 9)  # Start date for backtest
        self.SetEndDate(2024, 12, 10)   # End date for backtest
        self.SetCash(100000)           # Starting cash
        # Subscribe to custom stock data (replace with your actual symbol)
        self.stock_symbol = "AAPL"
        self.custom_symbol = self.AddData(StockDailyData, self.stock_symbol)  # Replace with the correct data name
        self.add_equity("AAPL", Resolution.DAILY)
        self.Debug(f"Custom symbol added: {self.custom_symbol}")

        self.received_data = []

    def on_data(self, data: Slice):
        """on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        if not self.portfolio.invested:
            self.set_holdings(self.custom_symbol, 1)
            self.debug("Purchased Stock")
        
        
        self.debug("OnData has been called")
        self.debug(f"Portfolio Value: {self.Portfolio.TotalPortfolioValue}")