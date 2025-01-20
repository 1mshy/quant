from AlgorithmImports import *

class RsiCrossoverAlgorithm(QCAlgorithm):
    def Initialize(self):
        # Set start and end dates for the backtest
        self.SetStartDate(2016, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)  # Starting cash

        # Add the asset
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Set up the RSI indicator
        self.rsi = self.RSI(self.symbol, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        # Track if we are invested
        self.is_invested = False

    def OnData(self, data):
        self.Debug(f"Date: {self.Time}, RSI: {self.rsi.Current.Value if self.rsi.IsReady else 'Not Ready'}")
        # Check if RSI is ready
        if not self.rsi.IsReady:
            return

        # Get the current RSI value
        rsi_value = self.rsi.Current.Value

        # Buy logic: RSI crosses above 30
        if rsi_value > 30 and not self.is_invested:
            self.SetHoldings(self.symbol, 1.0)  # Invest 100% of portfolio
            self.is_invested = True
            self.Debug(f"BUY: RSI crossed above 30. RSI={rsi_value:.2f}")

        # Sell logic: RSI crosses below 70
        elif rsi_value < 70 and self.is_invested:
            self.Liquidate(self.symbol)  # Sell all holdings
            self.is_invested = False
            self.Debug(f"SELL: RSI crossed below 70. RSI={rsi_value:.2f}")
