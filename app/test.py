from binance.spot import Spot as Client
from datetime import datetime
import os

# api_key and secret_key you get when you set up your API on Binance

api_key=os.environ.get('api_key')
api_secret=os.environ.get('api_secret')

spot_client = Client(api_key, secret_key)

currTime = round((time.time()*1000))
startTime = "01/01/2021"
beginTime = round(datetime.strptime(startTime, "%d/%m/%Y").timestamp()*1000)
params = {
      "beginTime": beginTime,
      "endTime": currTime
         }
# 0 = deposit, 1 = withdrawals
# if no beginTime and endTime specified will give last 30 days

spot_client.fiat_order_history(0, **params)