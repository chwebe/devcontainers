import requests

# Binance API URL for exchange information
BASE_URL = "https://api.binance.com"

def fetch_all_symbols():
    """
    Fetch all trading symbols directly from the Binance API.
    """
    url = f"{BASE_URL}/api/v3/exchangeInfo"
    try:
        # Send GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
        
        # Extract trading pairs that are currently active
        symbols = [
            symbol['symbol'] for symbol in data['symbols'] 
            if symbol['status'] == 'TRADING'
        ]
        return symbols
    except requests.exceptions.RequestException as e:
        print(f"Error fetching symbols: {e}")
        return None

# Fetch and print all trading pairs
symbols = fetch_all_symbols()

if symbols:
    print(f"Found {len(symbols)} trading pairs:")
    print(symbols)
else:
    print("Failed to fetch trading pairs.")
