from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import date
from datetime import datetime
import datetime
import time

cg = CoinGeckoAPI()
all_token = pd.read_csv('CoinGecko Token API List - CoinGecko Token API List.csv')
token_symbol = pd.DataFrame(str('BTC ETH BNB SOL ADA XRP LUNA AVAX DOT DOGE SHIB MATIC CRO LTC UNI LINK ALGO BCH TRX XLM MANA FTT AXS HBAR VET NEAR ATOM FIL EGLD ETC SAND ICP THETA XTZ HNT FTM XMR EOS GALA CAKE GRT ONE LRC BTT FLOW AAVE MKR KSM ENJ AR MIR CRV KDA RUNE BAT CHZ CVX YFI COMP 1INCH TFUEL OMG ENS IMX AUDIO BNT ILV PERP SUSHI ZRX ANC SNX RAY DYDX SRM MOVR YGG CHR ALPHA BAND REP SAND MANA AXS SLP PEOPLE').replace(' ',',').lower().split(","))

token_id = pd.merge(token_symbol,all_token,left_on=0,right_on='Symbol')
token_id = pd.DataFrame.drop_duplicates(token_id)
token_id_list = token_id['Id']
token_id_str = ','.join(token_id_list)

price = pd.DataFrame(cg.get_price(ids=token_id_str,vs_currencies='usd',include_market_cap='true', include_24hr_vol='true')).T.reset_index()
token_price = pd.merge(token_id,price,left_on='Id',right_on='index')[['Id','Symbol','Name','usd','usd_market_cap','usd_24h_vol']].rename(columns={'usd':'Price in USD','usd_market_cap':'Reported MktCap in USD','usd_24h_vol':'Real Volume in USD(24hrs)'})
token_price['Symbol'] = token_price['Symbol'].apply(lambda x: x.upper())

app_df = pd.read_csv('app_df.csv')
data_dash = pd.merge(token_price,app_df,left_on='Id',right_on='Unnamed: 0')
data_dash['12TD'] = data_dash['Price in USD']/data_dash['12TD']
data_dash['4QTD'] = data_dash['Price in USD']/data_dash['4QTD']
data_dash['2021TD'] = data_dash['Price in USD']/data_dash['2021TD']
data_dash = data_dash.drop(labels=['Id','Unnamed: 0'],axis=1)
for i in range(5,27):
    data_dash.iloc[:,i] = data_dash.iloc[:,i].apply(lambda x: format(x,'.2%'))
data_dash
