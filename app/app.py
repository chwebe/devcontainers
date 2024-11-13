from binance import Client
import os
import time
from datetime import datetime,timedelta

api_key=os.environ.get('api_key')
api_secret=os.environ.get('api_secret')


client = Client(api_key, api_secret)

#account_info = client.get_account()
#print(account_info)

# Function to retrieve deposit history within a time frame
def get_deposit_history_for_period(start_time, end_time):
    deposit_history = client.get_deposit_history(startTime=start_time, endTime=end_time)
    return deposit_history

# Start and end times
start_of_year = datetime(datetime.now().year, 1, 1)
current_time = datetime.now()

# Loop through the year in 90-day increments
all_deposits = []

while start_of_year < current_time:
    end_time = start_of_year + timedelta(days=90)
    if end_time > current_time:
        end_time = current_time
    
    start_time_ms = int(start_of_year.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)
    
    # Get deposits for this period
    deposits = get_deposit_history_for_period(start_time_ms, end_time_ms)
    print(f"Deposits from {start_of_year} to {end_time}")
    print(deposits)
    all_deposits.extend(deposits)
    
    # Move to the next 90-day period
    start_of_year = end_time

# Print all deposit details
for deposit in all_deposits:
    asset = deposit['asset']
    amount = deposit['amount']
    status = deposit['status']
    time = deposit['insertTime']
    print(f"Asset: {asset}, Amount: {amount}, Status: {status}, Time: {time}")
