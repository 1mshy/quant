import json
import os
from datetime import datetime
from yahoo import request_daily_stock_data

symbol = "SMCI"

# Input data
data = request_daily_stock_data(symbol)

# Output directory for the formatted data
output_dir = "../data/custom_csv_data/"
os.makedirs(output_dir, exist_ok=True)

csv_data = ""
# Process and write data
for record in data:    
    # Prepare formatted data
    formatted_record = {
        "date": datetime.utcfromtimestamp(record["datetime"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        "open": record["open"],
        "high": record["high"],
        "low": record["low"],
        "close": record["close"],
        "volume": record["volume"]
    }
    csv_data += f"{formatted_record['date']},{formatted_record['open']},{formatted_record['high']},{formatted_record['low']},{formatted_record['close']},{formatted_record['volume']}\n"
    

# Write to JSON file
with open(f"{output_dir}{symbol}.csv", "w") as f:
    f.write(csv_data)