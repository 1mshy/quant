from AlgorithmImports import *
from datetime import datetime
import os

SYMBOL = "AAPL"
DEFAULT_CASH = 100_000

class DescendingCustomDataObjectStoreRegressionAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(DEFAULT_CASH)
        self.settings.daily_precise_end_time = False # This is required to ensure the data is processed on the correct day
        self.SetBenchmark(lambda _: DEFAULT_CASH)  # No benchmark calculation, this will make requests to data we do not have access too
        #Possinle fields for self.SubscriptionManager
        # ['Add', 'AddConsolidator', 'AvailableDataTypes', 'Count', 'DefaultDataTypes', 'Equals', 'Finalize', 'GetDataTypesForSecurity', 
        # 'GetHashCode', 'GetType', 'IsSubscriptionValidForConsolidator', 'LookupSubscriptionConfigDataTypes', 'MemberwiseClone', 'Overloads', 'ReferenceEquals', 
        # 'RemoveConsolidator', 'ScanPastConsolidators', 'SetDataManager', 'SubscriptionDataConfigService', 'Subscriptions', 'ToString', '__class__', '__delattr__', '__dir__', 
        # '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', 
        # '__ne__', '__new__', '__overloads__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'add', 'add_consolidator', 
        # 'available_data_types', 'count', 'default_data_types', 'equals', 'finalize', 'get_AvailableDataTypes', 'get_Count', 'get_SubscriptionDataConfigService', 
        # 'get_Subscriptions', 'get_available_data_types', 'get_count', 'get_data_types_for_security', 'get_hash_code', 'get_subscription_data_config_service', 'get_subscriptions', 
        # 'get_type', 'is_subscription_valid_for_consolidator', 'lookup_subscription_config_data_types', 'memberwise_clone', 'reference_equals', 'remove_consolidator', 
        # 'scan_past_consolidators', 'set_data_manager', 'subscription_data_config_service', 'subscriptions', 'to_string']
        # self.Debug(dir(self.SubscriptionManager))
        # self.SubscriptionManager.RemoveAllSubscriptions()

        
        self.security = self.AddEquity(SYMBOL, Resolution.Daily, fillForward = False).Symbol

        # Add custom data for AAPL
        self.custom_symbol = self.AddData(SortCustomData, SYMBOL, Resolution.Daily).Symbol
        self.Debug(f"Custom symbol added: {self.custom_symbol}")

        self.received_data = []
        self.all_in_executed = False

    def OnData(self, slice):
        
        self.Debug(slice)

        # Check for custom data
        if slice.ContainsKey(self.custom_symbol):
            custom_data = slice[self.custom_symbol]
            self.Debug(f"Time: {custom_data.Time}, Close: {custom_data['Close']}")

            # Ensure data fields are valid
            if custom_data["Open"] == 0 or custom_data["High"] == 0 or custom_data["Low"] == 0 or custom_data["Close"] == 0:
                raise Exception("One or more custom data fields are zero.")

            self.received_data.append(custom_data)

            if self.all_in_executed:
                return
            # Go all in on AAPL when a certain condition is met (e.g., data length > 10)
            if len(self.received_data) > 10:
                # Calculate how many shares we can buy
                self.Debug(f"Received {self.received_data} entries. Going all in on AAPL.")
                self.Debug(f"Portfolio cash: {self.Portfolio.Cash}")
                self.Debug(f"Securities : {self.Securities[self.security].Price}")
                security_price = custom_data['Close']
                cash_available = self.Portfolio.Cash
                quantity = int(cash_available // security_price)

                if quantity > 0:
                    self.MarketOrder(self.security, quantity)
                    self.all_in_executed = True
                    self.Debug(f"Bought {quantity} shares of {SYMBOL} at {security_price}")

    def OnEndOfAlgorithm(self):
        if not self.received_data:
            raise Exception("No custom data received. Check the data source and subscription.")
        else:
            self.Debug(f"Custom data received: {len(self.received_data)} entries.")

class SortCustomData(PythonData):
    def get_source(self, config, date, is_live):
        symbol: str = config.Symbol.Value
        # Use the absolute path to the CSV file
        file_path = os.path.join(Globals.DataFolder, f"custom_csv_data/{SYMBOL}.csv")
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
