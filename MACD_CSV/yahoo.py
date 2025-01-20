import requests
import time

yahoo_base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"

def yahoo_url(symbol, range=None, interval="1d", period1=0, period2=int(time.time())):
    if range:
        return f"{yahoo_base_url}{symbol}?range={range}&interval={interval}"
    return f"{yahoo_base_url}{symbol}?period1={int(period1)}&period2={int(period2)}&interval={interval}"

def yahoo_to_structured(data):
    key_data = data['chart']['result'][0]
    timestamp = key_data['timestamp']
    events = key_data.get('events', {})
    meta = key_data['meta']
    indicators = key_data['indicators']['quote'][0]

    volume = indicators.get('volume', [])
    open_prices = indicators.get('open', [])
    high = indicators.get('high', [])
    close = key_data['indicators']['adjclose'][0]['adjclose']
    low = indicators.get('low', [])

    total_stock_data = {
        "data": [],
        "events": events,
        "meta": meta
    }

    for i in range(len(timestamp)):
        total_stock_data["data"].append({
            "datetime": timestamp[i] * 1000,  # converting to milliseconds
            "volume": volume[i] if i < len(volume) else None,
            "open": open_prices[i] if i < len(open_prices) else None,
            "high": high[i] if i < len(high) else None,
            "close": close[i] if i < len(close) else None,
            "low": low[i] if i < len(low) else None
        })

    return total_stock_data

def clean_ticker_for_yahoo(ticker):
    if not ticker:
        return ""
    return ticker.replace("/", "-").replace("^", "-").replace("*", "-").replace(".", "-").replace(",", "-")

def request_yahoo_big(ticker_symbol):
    print(f"Requesting {ticker_symbol}")
    url = yahoo_url(ticker_symbol)
    print(f"Requesting: {url}")

    headers = {
        "User-Agent": "PostmanRuntime/7.39.0",
        "Accept": "*/*",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"Invalid ticker symbol submitted: {ticker_symbol}")
        return {}

    return response.json()

def request_daily_stock_data(ticker_symbol):
    response = request_yahoo_big(ticker_symbol)
    return yahoo_to_structured(response)["data"]