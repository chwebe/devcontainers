from binance.spot import Spot as Client
from datetime import datetime
import os
import time


# api_key and secret_key you get when you set up your API on Binance

api_key=os.environ.get('api_key')
api_secret=os.environ.get('api_secret')

spot_client = Client(api_key,api_secret) 

currTime = round((time.time()*1000))
startTime = "14/07/2017"
beginTime = round(datetime.strptime(startTime, "%d/%m/%Y").timestamp()*1000)
params = {
      "beginTime": beginTime,
      "endTime": currTime
         }
# 0 = deposit, 1 = withdrawals
# if no beginTime and endTime specified will give last 30 days

#fiat_history = spot_client.fiat_order_history(0, **params)

fiat_history = {'code': '000000', 'message': 'success', 'data': [{'orderNo': 'OF5524217358754211841111', 'fiatCurrency': 'EUR', 'indicatedAmount': '10.00', 'amount': '9.00', 'totalFee': '1', 'method': 'Bank transfer(SEPA Instant)', 'status': 'Successful', 'createTime': 1731321355000, 'updateTime': 1731321355000}, {'orderNo': '03377553181145597952071784', 'fiatCurrency': 'EUR', 'indicatedAmount': '50.00', 'amount': '49.00', 'totalFee': '1', 'method': 'Offline Charge', 'status': 'Successful', 'createTime': 1689629442000, 'updateTime': 1689629442000}, {'orderNo': '03362622340515611648060684', 'fiatCurrency': 'EUR', 'indicatedAmount': '200.00', 'amount': '199.00', 'totalFee': '1', 'method': 'Offline Charge', 'status': 'Successful', 'createTime': 1686069652000, 'updateTime': 1686069652000}, {'orderNo': '03344706768972689408041884', 'fiatCurrency': 'EUR', 'indicatedAmount': '151.00', 'amount': '150.00', 'totalFee': '1', 'method': 'Offline Charge', 'status': 'Successful', 'createTime': 1681798247000, 'updateTime': 1681798247000}, {'orderNo': '03326786305432601600022784', 'fiatCurrency': 'EUR', 'indicatedAmount': '350.00', 'amount': '349.00', 'totalFee': '1', 'method': 'Offline Charge', 'status': 'Successful', 'createTime': 1677525676000, 'updateTime': 1677525675000}, {'orderNo': '03326783938733657088022784', 'fiatCurrency': 'EUR', 'indicatedAmount': '10.00', 'amount': '9.00', 'totalFee': '1', 'method': 'Offline Charge', 'status': 'Successful', 'createTime': 1677525111000, 'updateTime': 1677525111000}, {'orderNo': '03302345127358314496122284', 'fiatCurrency': 'EUR', 'indicatedAmount': '50.00', 'amount': '49.00', 'totalFee': '1', 'method': 'Offline Charge', 'status': 'Successful', 'createTime': 1671698445000, 'updateTime': 1671698444000}, {'orderNo': '2323636c275d442e9024a6ef9c6d079d', 'fiatCurrency': 'EUR', 'indicatedAmount': '100.00', 'amount': '100.00', 'totalFee': '0', 'method': 'Wallet', 'status': 'Expired', 'createTime': 1644875402000, 'updateTime': 1644875402000}, {'orderNo': '4d5163f51ae54c46aa9a3b97a87695ec', 'fiatCurrency': 'EUR', 'indicatedAmount': '50.00', 'amount': '50.00', 'totalFee': '0', 'method': 'Wallet', 'status': 'Expired', 'createTime': 1644517089000, 'updateTime': 1644517089000}, {'orderNo': 'c0ce6531ee0249fe9a240be12daa3ff8', 'fiatCurrency': 'EUR', 'indicatedAmount': '10.00', 'amount': '10.00', 'totalFee': '0', 'method': 'Wallet', 'status': 'Expired', 'createTime': 1644246724000, 'updateTime': 1644246724000}, {'orderNo': '85b9eb8c21c247129ea7c57d69c833b6', 'fiatCurrency': 'EUR', 'indicatedAmount': '50.00', 'amount': '50.00', 'totalFee': '0', 'method': 'Wallet', 'status': 'Expired', 'createTime': 1644223683000, 'updateTime': 1644223683000}, {'orderNo': 'a02a2c19c4714accbe4506b2fbb65d2f', 'fiatCurrency': 'EUR', 'indicatedAmount': '102.00', 'amount': '100.16', 'totalFee': '1.84', 'method': 'Card', 'status': 'Successful', 'createTime': 1638734083000, 'updateTime': 1638734129000}, {'orderNo': '3de57d9ce34540118af40f43e121ba5d', 'fiatCurrency': 'EUR', 'indicatedAmount': '100.00', 'amount': '98.20', 'totalFee': '1.8', 'method': 'Card', 'status': 'Successful', 'createTime': 1637526644000, 'updateTime': 1637526678000}, {'orderNo': '737af95f86a54407b3a03704f9220c82', 'fiatCurrency': 'EUR', 'indicatedAmount': '100.00', 'amount': '98.20', 'totalFee': '1.8', 'method': 'Card', 'status': 'Failed', 'createTime': 1637526274000, 'updateTime': 1637526291000}, {'orderNo': '831d2e98cc844b5b8ae0410c4a0004b6', 'fiatCurrency': 'EUR', 'indicatedAmount': '150.00', 'amount': '150.00', 'totalFee': '0', 'method': 'Card', 'status': 'Successful', 'createTime': 1628341572000, 'updateTime': 1628341602000}, {'orderNo': '397f25db046848a7a8829f56d56f4363', 'fiatCurrency': 'EUR', 'indicatedAmount': '50.00', 'amount': '50.00', 'totalFee': '0', 'method': 'Card', 'status': 'Successful', 'createTime': 1628341484000, 'updateTime': 1628341490000}, {'orderNo': '939f7d8e-e161-476f-81e4-02d9cf1232b7', 'fiatCurrency': 'EUR', 'indicatedAmount': '265.00', 'amount': '265.00', 'totalFee': '0', 'method': 'Bank Transfer', 'status': 'Successful', 'createTime': 1623133722000, 'updateTime': 1623134045000}, {'orderNo': '935db088-27e6-44fa-967a-9aa3a7d2c174', 'fiatCurrency': 'EUR', 'indicatedAmount': '200.00', 'amount': '200.00', 'totalFee': '0', 'method': 'Bank Transfer', 'status': 'Successful', 'createTime': 1620306647000, 'updateTime': 1620306971000}, {'orderNo': '9322e7d2-2e45-4495-87c1-575ebffe4adc', 'fiatCurrency': 'EUR', 'indicatedAmount': '150.00', 'amount': '150.00', 'totalFee': '0', 'method': 'Bank Transfer', 'status': 'Successful', 'createTime': 1617784490000, 'updateTime': 1617785243000}, {'orderNo': '92ee8927-c8e3-43cc-8f48-03194a5fcdfd', 'fiatCurrency': 'EUR', 'indicatedAmount': '75.00', 'amount': '75.00', 'totalFee': '0', 'method': 'Bank Transfer', 'status': 'Successful', 'createTime': 1615532833000, 'updateTime': 1615532930000}, {'orderNo': '92c0dcc4-7eea-4115-af21-a02d3d52d816', 'fiatCurrency': 'EUR', 'indicatedAmount': '50.00', 'amount': '50.00', 'totalFee': '0', 'method': 'Bank Transfer', 'status': 'Successful', 'createTime': 1613570767000, 'updateTime': 1613571040000}, {'orderNo': '92be446f-474e-4bde-a8a0-19fc255e6d50', 'fiatCurrency': 'EUR', 'indicatedAmount': '5.00', 'amount': '5.00', 'totalFee': '0', 'method': 'Bank Transfer', 'status': 'Successful', 'createTime': 1613460899000, 'updateTime': 1613462225000}], 'total': 22, 'success': True}

for order in fiat_history['data']:
    indicated_amount = float(order['indicatedAmount'])
    total_fee = float(order['totalFee'])
    result = indicated_amount - total_fee
    human_readable_time = datetime.fromtimestamp(order['createTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(human_readable_time)


deposit = spot_client.get_deposit_history(coin="USDT", status=1)
print(deposit)