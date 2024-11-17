import time
import os
import requests
import hmac
import hashlib
from urllib.parse import urlencode

# Binance API credentials
api_key=os.environ.get('api_key')
api_secret=os.environ.get('api_secret')
BASE_URL = "https://api.binance.com"

def create_signature(query_string, secret):
    """
    Create HMAC SHA256 signature for Binance API requests.
    """
    return hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def send_signed_request(endpoint, params):
    """
    Sends a signed GET request to the Binance API.
    """
    # Add timestamp to parameters
    params['timestamp'] = int(time.time() * 1000)

    # Generate signature
    query_string = urlencode(params)
    signature = create_signature(query_string, api_secret)
    params['signature'] = signature

    # Set headers
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Send request
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.json().get('msg', response.text)}")
    return response.json()

def get_trade_history(symbol, start_time, end_time, limit=500):
    """
    Fetch trade history for a specific trading pair over an extended time range.

    Parameters:
        symbol (str): Trading pair (e.g., 'EURUSDT').
        start_time (int): Start time in milliseconds since epoch.
        end_time (int): End time in milliseconds since epoch.
        limit (int): Number of trades to fetch per request (default 500, max 1000).

    Returns:
        list: Combined list of trades for the entire time range.
    """
    endpoint = "/api/v3/myTrades"
    results = []
    current_start = start_time
    one_day_ms = 24 * 60 * 60 * 1000  # 24 hours in milliseconds

    while current_start < end_time:
        # Set the end time for the current chunk (max 24 hours)
        current_end = min(current_start + one_day_ms, end_time)

        # Prepare request parameters
        params = {
            "symbol": symbol,
            "startTime": current_start,
            "endTime": current_end,
            "limit": limit,
        }

        # Send request
        data = send_signed_request(endpoint, params)

        # Append the trades from the response
        results.extend(data)

        # Move to the next time chunk
        current_start = current_end

    return results

# Example usage
if __name__ == "__main__":
    try:
        # Define trading pair and time range
        symbol = "EURUSDT"
        start_time = int(time.mktime(time.strptime("2020-01-01", "%Y-%m-%d")) * 1000)  # Start: Jan 1, 2020
        end_time = int(time.time() * 1000)  # Current time

        trades = get_trade_history(symbol, start_time=start_time, end_time=end_time)
        print("Trades:", trades)
    except Exception as e:
        print("Error:", e)


[{'symbol': 'EURUSDT', 'id': 87518702, 'orderId': 260147435, 'orderListId': -1, 'price': '1.05420000', 'qty': '50.00000000', 'quoteQty': '52.71000000', 'commission': '0.00012990', 'commissionAsset': 'BNB', 'time': 1677536046425, 'isBuyer': False, 'isMaker': False, 'isBestMatch': True}, {'symbol': 'EURUSDT', 'id': 87518730, 'orderId': 260147548, 'orderListId': -1, 'price': '1.05410000', 'qty': '308.00000000', 'quoteQty': '324.66280000', 'commission': '0.00080044', 'commissionAsset': 'BNB', 'time': 1677536073480, 'isBuyer': False, 'isMaker': False, 'isBestMatch': True}, {'symbol': 'EURUSDT', 'id': 91523706, 'orderId': 274049341, 'orderListId': -1, 'price': '1.09140000', 'qty': '150.00000000', 'quoteQty': '163.71000000', 'commission': '0.00035578', 'commissionAsset': 'BNB', 'time': 1681798340521, 'isBuyer': False, 'isMaker': False, 'isBestMatch': True}, {'symbol': 'EURUSDT', 'id': 95075060, 'orderId': 285800457, 'orderListId': -1, 'price': '1.06550000', 'qty': '199.00000000', 'quoteQty': '212.03450000', 'commission': '0.00056252', 'commissionAsset': 'BNB', 'time': 1686075684491, 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}]