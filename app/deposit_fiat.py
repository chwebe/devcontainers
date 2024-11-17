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

def get_fiat_orders(transaction_type, start_time, end_time, rows=500):
    """
    Fetch fiat orders from Binance API for a specified time range.
    Automatically handles paginated requests if results exceed the max rows.

    Parameters:
        transaction_type (int): 0 for deposit, 1 for withdraw.
        start_time (int): Start time in milliseconds since epoch.
        end_time (int): End time in milliseconds since epoch.
        rows (int): Number of rows per request (max 500).

    Returns:
        list: Combined list of fiat orders for the specified range.
    """
    endpoint = "/sapi/v1/fiat/orders"
    results = []
    max_rows = rows
    page = 1

    while True:
        # Prepare request parameters
        params = {
            "transactionType": transaction_type,
            "beginTime": start_time,
            "endTime": end_time,
            "page": page,
            "rows": max_rows,
        }

        # Send request
        data = send_signed_request(endpoint, params)

        # Append results
        results.extend(data.get("data", []))

        # Check if there are more pages
        total_records = data.get("total", 0)
        if len(results) >= total_records or len(data.get("data", [])) < max_rows:
            break

        # Increment page for the next request
        page += 1

    return results

# Example usage
if __name__ == "__main__":
    try:
        # Start time: January 1, 2020
        start_time = int(time.mktime(time.strptime("2020-01-01", "%Y-%m-%d")) * 1000)
        # End time: Current time
        end_time = int(time.time() * 1000)

        # Fetch deposit orders
        deposits = get_fiat_orders(transaction_type=0, start_time=start_time, end_time=end_time)
        for order in deposits:
            print(f"Order No: {order['orderNo']}, Amount: {order['amount']} {order['fiatCurrency']}")
        
    except Exception as e:
        print("Error:", e)

