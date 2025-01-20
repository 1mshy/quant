import json
import os
from datetime import datetime
from yahoo import request_daily_stock_data
# Input data
data = request_daily_stock_data("AAPL")

# Output directory for the formatted data
output_dir = "custom_data"
os.makedirs(output_dir, exist_ok=True)

# Process and write data
for record in data:
    # Convert timestamp to date
    date = datetime.utcfromtimestamp(record["datetime"] / 1000).strftime("%Y%m%d")
    
    # Prepare formatted data
    formatted_record = {
        "date": datetime.utcfromtimestamp(record["datetime"] / 1000).strftime("%Y-%m-%d"),
        "open": record["open"],
        "high": record["high"],
        "low": record["low"],
        "close": record["close"],
        "volume": record["volume"]
    }
    
    # File path for the current date
    file_path = os.path.join(output_dir, f"{date}.json")
    
    # Write to JSON file
    with open(file_path, "w") as f:
        json.dump(formatted_record, f, indent=None)

print(f"Data has been processed and saved to {output_dir}")
