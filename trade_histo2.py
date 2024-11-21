import os 
from binance.client import Client

api_key=os.environ.get('api_key')
api_secret=os.environ.get('api_secret')
client = Client(api_key, api_secret)

def fetch_trade_history():
    trades = []
    symbols = [symbol['symbol'] for symbol in client.get_exchange_info()['symbols']]
    for symbol in symbols:
        try:
            trades.extend(client.get_my_trades(symbol=symbol))
        except Exception as e:
            print(f"Error fetching trades for {symbol}: {e}")
    return trades


deposit_data = fetch_trade_history()
print(deposit_data)