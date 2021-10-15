#!/usr/bin/env python
# coding: utf-8

# In[10]:


get_ipython().run_line_magic('pip', 'install python-binance')


# In[1]:


import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager


# In[2]:


client = Client('api-key', 'api-secret')


# In[3]:


bsm = BinanceSocketManager(client)


# In[4]:


socket = bsm.trade_socket('BTCUSDT')


# In[7]:


while True:
    await socket.__aenter__()
    msg = await socket.recv()
    frame = createDataFrame(msg)
    frame.to_sql('BTCUSDT', engine, if_exists='append', index = False)
    print(frame)


# In[5]:


def createDataFrame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol','Time','Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


# In[ ]:


createDataFrame(msg)


# In[6]:


engine = sqlalchemy.create_engine('sqlite:///BTCUSDTsream.db')


# In[ ]:




