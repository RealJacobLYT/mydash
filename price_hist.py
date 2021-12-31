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


app_index = ['1/2021','2/2021','3/2021','4/2021','5/2021','6/2021','7/2021','8/2021','9/2021','10/2021','11/2021','12TD','1Q21','2Q21','3Q21','4QTD','2016','2017','2018','2019','2020','2021TD']
date_list = pd.Series(['2015-12-31','2016-12-31','2017-12-31','2018-12-31','2019-12-31','2020-12-31','2021-01-31','2021-02-28','2021-03-31','2021-04-30','2021-05-31','2021-06-30','2021-07-31','2021-08-31','2021-09-30','2021-10-31','2021-11-30'])
#price_hist = pd.DataFrame(pd.DataFrame(cg.get_coin_history_by_id(id='bitcoin',date='01-01-2020',vs_currencies='usd'))['market_data']['current_price'],index=[0])
# price_hist = pd.DataFrame(cg.get_coin_market_chart_by_id(id='bitcoin',vs_currency='usd',days='max'))
# price_hist['date'] = price_hist['prices'].map(lambda x: time.strftime("%Y-%m-%d",time.localtime(x[0]/1000)))
# price_hist['price'] = price_hist['prices'].map(lambda x: x[1])
# price_hist = pd.merge(date_list.to_frame('0'),price_hist,left_on='0',right_on='date')[['date','price']]
# t = price_hist['price']
# appreciation = pd.Series(data=['bitcoin',t[6]/t[5]-1,t[7]/t[6]-1,t[8]/t[7]-1,t[9]/t[8]-1,t[10]/t[9]-1,t[11]/t[10]-1,t[12]/t[11]-1,t[13]/t[12]-1,t[14]/t[13]-1,t[15]/t[14]-1,t[16]/t[15]-1,t[16],t[8]/t[5]-1,t[11]/t[8]-1,t[14]/t[11]-1,t[14],t[1]/t[0]-1,t[2]/t[1]-1,t[3]/t[2]-1,t[4]/t[3]-1,t[5]/t[4]-1,t[6]],index=app_index)

app_df = pd.DataFrame(data=None,index=app_index)
for i in token_id_list[96:]:
    price_hist = pd.DataFrame(cg.get_coin_market_chart_by_id(id=i, vs_currency='usd', days='max'))
    price_hist['date'] = price_hist['prices'].map(lambda x: time.strftime("%Y-%m-%d", time.localtime(x[0] / 1000)))
    price_hist['price'] = price_hist['prices'].map(lambda x: x[1])
    price_hist = pd.merge(date_list.to_frame('0'), price_hist, left_on='0', right_on='date',how='left')[['date', 'price']]
    t = price_hist['price']
    appreciation = pd.DataFrame(
        data=[t[6] / t[5] - 1, t[7] / t[6] - 1, t[8] / t[7] - 1, t[9] / t[8] - 1, t[10] / t[9] - 1,
              t[11] / t[10] - 1, t[12] / t[11] - 1, t[13] / t[12] - 1, t[14] / t[13] - 1, t[15] / t[14] - 1,
              t[16] / t[15] - 1, t[16], t[8] / t[5] - 1, t[11] / t[8] - 1, t[14] / t[11] - 1, t[14], t[1] / t[0] - 1,
              t[2] / t[1] - 1, t[3] / t[2] - 1, t[4] / t[3] - 1, t[5] / t[4] - 1, t[6]], index=app_index)
    app_df[i] = appreciation

app_df.T.to_csv('app_df.csv')
