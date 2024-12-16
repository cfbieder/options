# %%
#Load required libraries
import pandas as pd
import yfinance as yf
import math
import statistics
import json
from openbb import obb
from scipy import stats
from datetime import date, timedelta
from matplotlib import pyplot as plt
from datetime import date, timedelta
from datetime import date, timedelta


class Evaluator:

    def __init__(self):
        #!pip install yfinance
        #!pip install matplotlib
        #!pip install scipy

        df = pd.read_fwf("call.txt",skiprows=38)
        self.df_call = df.drop(df.loc[df['Symb'].str.contains('Symb')].index)
        self.df_call['AERTNC'] = self.df_call['AERTNC'].astype(float)
        self.df_call['PrDBE'] = self.df_call['PrDBE'].astype(float)
        self.df_call['PrRIE'] = self.df_call['PrRIE'].astype(float)
        self.df_call['PrUBE'] = self.df_call['PrUBE'].astype(float)


    def getQuote(self,ticker):
        stock = yf.Ticker(ticker)
        qType = stock.info['quoteType']
        print (json.dumps(stock.info, indent=4))
        price = (stock.info['bid']+stock.info['ask'])/2
        print (price)

    def getGraph(self,ticker, period = 30):
        start = date.today() - timedelta(period)
        start.strftime('%Y-%m-%d')
        end = date.today() + timedelta(2)
        end.strftime('%Y-%m-%d')
        stock_data = yf.download(ticker,start=start,end=end)
        plt.figure(figsize=(10,5))
        plt.plot(stock_data['Close'], label="Close")
        plt.title(ticker+" Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.legend()
        plt.grid(True)
        plt.show()

    def avgReturn(self,ticker,period=100,plot=1):
        start = date.today() - timedelta(period)
        start.strftime('%Y-%m-%d')
        end = date.today() + timedelta(2)
        end.strftime('%Y-%m-%d')
        stock = yf.download(ticker, start, end)
        stock = stock.dropna()
        stock['daily_percent_change'] = stock['Adj Close'].pct_change()
        mean = stock['daily_percent_change'].mean()
        sd = stock['daily_percent_change'].std()


        if (plot):
            plt.figure(figsize=(10,7))
            amzn_plt = plt.hist(stock['daily_percent_change'], bins = 50, histtype = 'bar', rwidth = 0.8)
            plt.title('Normal Distribution')
            plt.ylabel('Frequency')
            plt.xlabel('Daily Percentage Change')
            plt.show()

        print (mean,sd,sd*math.sqrt(252))

    def test(self):
        #print (df.info())
        #print (self.df_call.keys())
        #print (df2.info())
        #print (df_call.head())
        print ("TEST2")

    def screenCC(self,prDBE=80,prRIE=20,prUBE=5,aERTNC=20):
        # Probability of being above the downside breakeven point at expiration (PrDBE)
        # fairly high downside protection (PrDBE) – say nearly 60% or more,
        #prDBE = 80
        #Probability of being called away, or making the Return If Exercised (PrRIE)
        #a reasonable expectation of being called away (PrRIE) – say 20% or more
        #prRIE = 20
        #Probability of being above the upside breakeven point at expiration (PrUBE)
        # and a PrUBE of at least 5% less than the PrRIE,
        #prUBE = 5
        # Expected Return
        #aERTNC = 15
        
        rslt_df = self.df_call[(self.df_call['AERTNC'] >= aERTNC) & (self.df_call['PrDBE'] >= prDBE) & (self.df_call['PrRIE'] >= prRIE) & ((self.df_call['PrRIE'] - self.df_call['PrUBE']) >=prUBE )  ]
        print (rslt_df[['Symb','Stk','Opt  StrkMn','Call','AERTNC','PrDBE','PrRIE','PrUBE','Invt']])




# %%
evaluator = Evaluator()
ticker = 'LLY'
evaluator.getQuote(ticker)
# %%
evaluator.getGraph(ticker)
# %%
