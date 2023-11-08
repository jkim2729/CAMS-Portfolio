# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 22:21:17 2023

@author: Jacob Kim
"""
from enum import Enum  # Standard Python Library
import time, os, sys  # Standard Python Library
import xlwings as xw  # pip install xlwings
import pandas as pd  # pip install pandas
import yfinance as yf # pip install yahoofinancials
from datetime import date


def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    #Create a Dataframe
    df = pd.DataFrame()
    new_row = {
            'Shares':'',
            "Purchase Price":'',
            'Current Price':''
                 }
    df = df.append(new_row, ignore_index=True)
    tickers = sheet.range("C7").options(expand='down').value
    short_purchase_data = sheet.range('G36').options(expand='down').value
    short_tickers = sheet.range("C36").options(expand='down').value
    purchase_data = sheet.range('G7').options(expand='down').value
    short_shares = sheet.range('E36').options(expand='down').value
    reinvest_dividends = sheet.range('F7').options(expand='down').value
    shares = sheet.range('E7').options(expand='down').value
    counter = 1
    short_counter = 1 
    for tck in tickers:
        #Get data from Yahoo Finance
         if tck is not None:
             #Get data from Yahoo Finance
             data = yf.Ticker(tck).history(interval = '1d',start=(purchase_data[counter]),end =date.today())

             purchase_price = data.Close.iloc[0]
             current_price = data.Close.iloc[-1]
             num_shares = shares[counter]
             if reinvest_dividends[counter] == 'Y':
                 for j in range(len(data)+1):
                     if j == len(data):
                         break
                     if data.Dividends.iloc[j]!=0:
                         num_shares+= data.Dividends.iloc[j]/(data.Open.iloc[j+1])
             #Create dictionary info
             new_row = {
                 'Shares':num_shares,
                 "Purchase Price":purchase_price,
                 'Current Price':current_price
                 }
             #append data to data frame
             df = df.append(new_row, ignore_index=True)
             counter+=1
    sheet.range('H6').options(index=False).value = df
    # for tck in short_tickers:
    #     if tck is not None: 
    #         short_data = yf.Ticker(tck).history(interval = '1d',start=(purchase_data[counter]),end =date.today())
    #         purchase_price = short_data.Close.iloc[0]
    #         current_price = short_data.Close.iloc[-1]
    #         num_shares = short_shares[short_counter]
    #         new_row = {
    #               'Shares':num_shares,
    #               "Purchase Price":purchase_price,
    #               'Current Price':current_price
    #               }
    #           #append data to data frame
    #         df = df.append(new_row, ignore_index=True)
    #         short_counter+=1
    # sheet.range('H36').options(index=False).value = df
            


@xw.func
def hello(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    xw.Book("portfolio.xlsm").set_mock_caller()
    main()



    
