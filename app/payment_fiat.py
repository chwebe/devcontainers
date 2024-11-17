import time
import requests
import hmac
import hashlib
import os 
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

def get_fiat_payments_history(transaction_type, begin_time=None, end_time=None, page=1, rows=100):
    """
    Fetch Fiat Payments History for deposit or withdrawal.

    Parameters:
        transaction_type (str): Type of transaction (0 for buy, 1 for sell).
        begin_time (int): Start time in milliseconds since epoch (optional).
        end_time (int): End time in milliseconds since epoch (optional).
        page (int): Page number for pagination (default 1).
        rows (int): Number of rows to fetch per request (default 100, max 500).

    Returns:
        dict: JSON response from the Binance API with fiat payments history.
    """
    endpoint = "/sapi/v1/fiat/payments"
    params = {
        "transactionType": transaction_type,
        "page": page,
        "rows": rows
    }
    if begin_time:
        params["beginTime"] = begin_time
    if end_time:
        params["endTime"] = end_time

    return send_signed_request(endpoint, params)

# Example usage
if __name__ == "__main__":
    try:
        # Define transaction type and optional date range
        transaction_type = "0"  # 0 for buy, 1 for sell
        begin_time = int(time.mktime(time.strptime("2023-01-01", "%Y-%m-%d")) * 1000)  # Start: Jan 1, 2023
        end_time = int(time.time() * 1000)  # Current time

        payments_history = get_fiat_payments_history(transaction_type, begin_time=begin_time, end_time=end_time)
        print("Payments History:", payments_history)
    except Exception as e:
        print("Error:", e)
