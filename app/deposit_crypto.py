import os
import time
import requests
import hmac
import hashlib
from urllib.parse import urlencode



# Get API key and secret from environment variables
api_key=os.environ.get('api_key')
api_secret=os.environ.get('api_secret')

# Binance API base URL
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

# deposit crypto
def get_deposit_history(coin=None, status=None, start_time=None, end_time=None, include_source=False):
    """
    Fetch deposit history from Binance API, handling extended date ranges.
    """
    endpoint = "/sapi/v1/capital/deposit/hisrec"
    results = []
    limit = 1000  # Max limit per request
    max_interval = 90 * 24 * 60 * 60 * 1000  # 90 days in milliseconds
    current_start_time = start_time

    while True:
        # Calculate the interval for the current request
        current_end_time = min(current_start_time + max_interval - 1, end_time) if current_start_time else end_time

        # Prepare request parameters
        params = {
            "limit": limit,
            "includeSource": str(include_source).lower(),
        }
        if coin:
            params["coin"] = coin
        if status is not None:
            params["status"] = status
        if current_start_time:
            params["startTime"] = current_start_time
        if current_end_time:
            params["endTime"] = current_end_time

        # Send the request
        data = send_signed_request(endpoint, params)

        # Append results
        results.extend(data)

        # If fewer results returned than limit, or we’ve reached the end, stop
        if len(data) < limit or current_end_time >= end_time:
            break

        # Move to the next interval
        current_start_time = current_end_time + 1

    return results

# Example usage
if __name__ == "__main__":
    try:
        deposits = get_deposit_history(
            status=1,  # Successful deposits
            start_time=1622505600000,  # Example: June 1, 2021
            end_time=int(time.time() * 1000),  # Present time
            include_source=True
        )
        print("Deposits:", deposits)
    except Exception as e:
        print("Error:", e)
