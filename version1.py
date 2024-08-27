##아나콘다 설치 후 환경을 분리해야 필요한 패키지를 따로 받을 필요가 없다.
##아나콘다는 조건부 무료이기 때문에 주의하자.
##비주얼코드 환경을 글로벌 또는 맞춤에서 base:conda로 바꾸어야 한다. 

import requests
import pandas as pd
import json
from openpyxl import load_workbook

print("binance list")

url='https://api.binance.com/api/v3/exchangeInfo'

response = requests.get(url)
data = json.loads(response.text)

#print(data)

symbols = data['symbols']
spot=[]
for symbol in symbols:
    if symbol['quoteAsset']=='USDT':
        spot.append(symbol['symbol'])

#print(spot)

binance_list = [x.replace("USDT","") for x in spot]

print(binance_list)

#upbit

print("upbit_list")

url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

#print(response.text)

data = response.json()

upbit_list = [item['market'] for item in data if 'market' in item]

# 각 통화별로 리스트 분리
upbit_krw_list = [item for item in upbit_list if item.startswith('KRW')]
upbit_btc_list = [item for item in upbit_list if item.startswith('BTC')]
upbit_usdt_list = [item for item in upbit_list if item.startswith('USDT')]

upbit_krw_list = [item.split('-')[1] for item in upbit_list if item.startswith('KRW')]
upbit_btc_list = [item.split('-')[1] for item in upbit_list if item.startswith('BTC')]
upbit_usdt_list = [item.split('-')[1] for item in upbit_list if item.startswith('USDT')]

print(upbit_list)

#bithumb

print("bitumb list")

url = "https://api.bithumb.com/public/assetsstatus/ALL"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

data = response.json()

assets = data['data']

bithumb_list = [name for name, details in assets.items()
                   if details['withdrawal_status'] == 1 and details['deposit_status'] == 1]

print(bithumb_list)

#coinone

import requests

print("coinone list")

url = "https://api.coinone.co.kr/public/v2/markets/KRW"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

data = response.json()

markets = data['markets']

coinone_list = [f"{item['target_currency']}" for item in markets]

print(coinone_list)

#코빗

print("korbit_list")

url = "https://api.korbit.co.kr/v1/ticker/detailed/all"

response = requests.get(url)

data = response.json()

korbit_list = [f"{pair.split('_')[0]}".upper() for pair in data.keys()]

print(korbit_list)

# 리스트들의 길이를 동일하게 맞추기
max_length = max(len(binance_list), len(upbit_list), len(bithumb_list), len(coinone_list), len(korbit_list))
binance_list.extend([None] * (max_length - len(binance_list)))
upbit_list.extend([None] * (max_length - len(upbit_list)))
bithumb_list.extend([None] * (max_length - len(bithumb_list)))
coinone_list.extend([None] * (max_length - len(coinone_list)))
korbit_list.extend([None] * (max_length - len(korbit_list)))
upbit_krw_list.extend([None] * (max_length - len(upbit_krw_list)))
upbit_btc_list.extend([None] * (max_length - len(upbit_btc_list)))
upbit_usdt_list.extend([None] * (max_length - len(upbit_usdt_list)))

df=pd.DataFrame({'Binance' : binance_list, 'Upbit-krw' :upbit_krw_list, 'Upbit-btc' :upbit_btc_list, 'Upbit-usdt' :upbit_usdt_list, 'Bithumb' : bithumb_list, 'Coinone':coinone_list, 'Korbit': korbit_list})
df.to_excel('public_list.xlsx', index=False)