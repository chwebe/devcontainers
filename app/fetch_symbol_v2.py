import requests
import hmac
import hashlib
import time
import os 
from concurrent.futures import ThreadPoolExecutor, as_completed

# Binance API keys (replace with your keys)
API_KEY = os.environ.get('api_key')
API_SECRET = os.environ.get('api_secret')
BASE_URL = "https://api.binance.com"

# Function to create a Binance API signature
def create_signature(query_string, secret):
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

# Fetch trade history for a specific symbol
def fetch_my_trades(symbol):
    """
    Fetch trade history for a given symbol using Binance API.
    """
    endpoint = "/api/v3/myTrades"
    url = BASE_URL + endpoint

    # Query parameters
    params = {
        "symbol": symbol,
        "limit": 1000,
        "timestamp": int(time.time() * 1000),
    }

    # Create query string
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    signature = create_signature(query_string, API_SECRET)
    params["signature"] = signature

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        # Track rate limit usage
        used_weight = response.headers.get("X-MBX-USED-WEIGHT-1M", "0")
        return response.json(), int(used_weight)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trades for {symbol}: {e}")
        return None, 0

# Function to monitor and throttle requests
def monitor_rate_limit(used_weight):
    """
    Throttle requests if close to the rate limit.
    """
    if used_weight >= 1100:  # Close to the 1200 limit
        print("Approaching rate limit. Pausing...")
        time.sleep(60)  # Wait for the rate limit window to reset

# Parallel fetching of trade data
def fetch_all_trades_parallel(symbols):
    """
    Fetch trades for all symbols in parallel, respecting rate limits.
    """
    all_trades = []
    total_weight = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_my_trades, symbol): symbol for symbol in symbols}

        for future in as_completed(futures):
            symbol = futures[future]
            try:
                trades, used_weight = future.result()
                if trades:
                    all_trades.extend(trades)
                total_weight += used_weight
                print(f"Fetched trades for {symbol}. Current weight: {total_weight}")

                # Monitor and throttle if rate limit is near
                monitor_rate_limit(total_weight)
            except Exception as e:
                print(f"Error with {symbol}: {e}")

    return all_trades

# Fetch all active trading pairs
def fetch_all_symbols():
    """
    Fetch all trading symbols directly from the Binance API.
    """
    url = f"{BASE_URL}/api/v3/exchangeInfo"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        symbols = [
            symbol['symbol'] for symbol in data['symbols'] 
            if symbol['status'] == 'TRADING'
        ]
        return symbols
    except requests.exceptions.RequestException as e:
        print(f"Error fetching symbols: {e}")
        return None

# Main script
if __name__ == "__main__":
    symbols = fetch_all_symbols()  # Get all symbols
    if symbols:
        print(f"Found {len(symbols)} symbols. Fetching trades...")
        all_trades = fetch_all_trades_parallel(symbols[:20])  # Limit to first 20 for testing
        print(f"Fetched {len(all_trades)} trades in total.")
    else:
        print("No symbols found.")
