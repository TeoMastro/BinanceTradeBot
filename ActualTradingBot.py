#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlalchemy
import pandas as pd
from binance.client import Client


# In[2]:


client = Client('api-key', 'api-secret')


# In[4]:


engine = sqlalchemy.create_engine('sqlite:///BTCUSDTsream.db')


# In[5]:


df = pd.read_sql('BTCUSDT', engine)


# In[6]:


df


# In[7]:


df.Price.plot()


# In[8]:


def strategy(entry, lookback, qty, open_position=False):
    while True: 
        df = pd.read_sql('BTCUSDT', engine)
        lookbackperiod = df.iloc[-lookback:] #vriskei to pio palio timestamp
        cumret = (lookbackperiod.Price.pct_change() +1).cumprod()-1 #cummulative return, h teleutaia timh toy coin
        if not open_position:
            if cumret[cumret.last_valid_index()] > entry: #check an to cummylative return > entry price
                order = client.create_order(symbol='BTCUSDT', side = 'BUY', type = 'MARKET' , quantity=qty)
                print(order)
                open_position = True
                break
    if open_position:
        while True:
            df = pd.read_sql('BTCUSDT', engine)
            sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'],unit='ms')] #filter gia mono ton xrono ap ton opoio agorasame to asset kai meta
            
            if len(sincebuy) > 1: 
                sincebuyret = (sincebuy.Price.pct_change() +1).cumprod()-1 #o typos gia na dw thn epistrofh poy exw, idios me panw
                last_entry = sincebuyret[sincebuyret.last_valid_index()]
                if last_entry > 0.0015 or last_entry < -0.0015:
                    order = client.create_order(symbol='BTCUSDT', side = 'BUY', type = 'MARKET' , quantity=qty)
                    print(order)
                    break


# In[9]:


strategy(0.001, 60, 0.001)


# In[ ]:




