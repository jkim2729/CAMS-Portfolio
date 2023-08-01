# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 22:21:17 2023

@author: Jacob Kim
"""
import yfinance as yf
import pandas as pd
from datetime import date

original_port = {
    'AAPL': {'Shares': 10,'Purchase Date': '2022-01-15', 'Reinvest Dividends': 'Yes', 'Dividend Earnings': 0, 'Long or Short': 'Long'},
    'F': {'Shares': 5,'Purchase Date': '2022-02-10','Reinvest Dividends': 'Yes', 'Dividend Earnings': 0, 'Long or Short': 'Long'},
    'MSFT': {'Shares': 8,'Purchase Date': '2022-03-20','Reinvest Dividends': 'Yes', 'Dividend Earnings': 0, 'Long or Short': 'Short'},
    # Add more stocks if needed
}


portfolio = {
    'AAPL': {'Shares': 10,'Purchase Date': '2022-01-15', 'Reinvest Dividends': 'Yes', 'Dividend Earnings': 0, 'Long or Short': 'Long'},
    'F': {'Shares': 5,'Purchase Date': '2022-02-10','Reinvest Dividends': 'Yes', 'Dividend Earnings': 0, 'Long or Short': 'Long'},
    'MSFT': {'Shares': 8,'Purchase Date': '2022-03-20','Reinvest Dividends': 'Yes', 'Dividend Earnings': 0, 'Long or Short': 'Short'},
    # Add more stocks if needed
}


def get_portfolio_data(portfolio):
    x = list(portfolio.keys())
    data = yf.Ticker(x[0]).history(interval = '1d',start=(portfolio[x[0]]['Purchase Date']),end =date.today())
    for i in range(1,len(x)):
        newdata = yf.Ticker(x[i]).history(interval = '1d',start=(portfolio[x[0]]['Purchase Date']),end=date.today())
        data = pd.concat([data, newdata], axis=1)
        
    return data
def update_dividends(portfolio_data):
    y = list(portfolio.keys())
    for i in range(len(y)):
        if (portfolio[y[i]]['Reinvest Dividends'] == 'Yes') and (portfolio[y[i]]['Long or Short'] == 'Long'):
            for j in range(len(portfolio_data)+1):
                if j == len(portfolio_data):
                    break
                if portfolio_data.Dividends.iloc[j,i]!=0:
                    portfolio[y[i]]['Shares']+= portfolio_data.Dividends.iloc[j,i]/(portfolio_data.Open.iloc[j+1,i])
    return portfolio
    
        
        
def calculate_portfolio_value(portfolio_data, updated_portfolio):
    z = list(portfolio.keys())
    portfolio_value ={}
    for t in portfolio.keys():
        portfolio_value.update({t:{'Shares': updated_portfolio[t]['Shares'],'Current Value': ''}})
    for i in range(len(z)):
        if (portfolio[z[i]]['Long or Short'] == 'Long'):
            portfolio_value[z[i]]['Current Value'] = portfolio_value[z[i]]['Shares']*portfolio_data.Close.iloc[-1,i] + updated_portfolio[z[i]]['Dividend Earnings'] 
            portfolio_value[z[i]]['Gain/Loss'] = portfolio_value[z[i]]['Current Value'] - original_port[z[i]]['Shares']*portfolio_data.Open.iloc[0,i]
        elif (portfolio[z[i]]['Long or Short'] == 'Short'):
            portfolio_value[z[i]]['Current Value'] = portfolio_value[z[i]]['Shares']*portfolio_data.Close.iloc[-1,i]
            portfolio_value[z[i]]['Gain/Loss'] = original_port[z[i]]['Shares']*portfolio_data.Open.iloc[0,i] - portfolio_value[z[i]]['Current Value']
    return portfolio_value

         



    
