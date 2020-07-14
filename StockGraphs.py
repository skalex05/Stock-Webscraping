# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 10:33:38 2019

@author: AlexD
"""

import os,matplotlib, datetime, time, WebScraper, requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
from Stocks import Stocks

labelFont = {
        "fontname": "Arial",
        "size": 5
        }

data = []

def AddStock(name,htmlLink):
    try:
        response = requests.get(htmlLink)
    except Exception as err:
        print("Failed to add. Please try again.")
    htmlDoc = response.text
    try:
        soup = BeautifulSoup(htmlDoc,"html.parser")
        divs = soup.find_all("div",{"id":"app"})[0]     
        spans = divs.find_all("span")
    except Exception:
        pass
    for i in range(0,len(spans)):
        try:
            x = float(spans[i].text)
            Stocks[name] = [htmlLink,i]
            break
        except Exception:
            pass
    
    string = """Stocks = {
    """
    for key,val in Stocks.items():
        print(key)
        string = string +"'"+key+"':"+str(val)+""",
    """
    string += "}"
    file = open("Stocks.py","w+")
    file.write(string)
    file.close()
        
    
 
def GetStockGraph(name,yAxis,timeframe = "Ever"):
    lastStockPrice = 0
    xAxis = "DateTime"
    stockPrice = WebScraper.ShowStockData(name,Stocks[name][0],Stocks[name][1])
    os.startfile(os.getcwd()+"/"+name+"/index.html")
    while True:
        try:
            stockPrice = WebScraper.ShowStockData(name,Stocks[name][0],Stocks[name][1])
            if stockPrice == None:
                continue
            if stockPrice != lastStockPrice:
                print("--Stock Update--")
                lastStockPrice = stockPrice
                dataset = pd.read_csv(name+"/stockData.csv")
                if timeframe == "Minute":
                    dataset = dataset[dataset[xAxis] > matplotlib.dates.date2num(datetime.datetime.now() - datetime.timedelta(minutes = 1))]
                elif timeframe == "Hour":
                    print("Hour")
                    dataset = dataset[dataset[xAxis] > matplotlib.dates.date2num(datetime.datetime.now() - datetime.timedelta(hours = 1))]
                elif timeframe == "Day":
                    dataset = dataset[dataset[xAxis] > matplotlib.dates.date2num(datetime.datetime.now() - datetime.timedelta(hours = 24))]
                elif timeframe == "Month":
                    dataset = dataset[dataset[xAxis] > matplotlib.dates.date2num(datetime.datetime.now() - datetime.timedelta(hours = 24*30))]
                elif timeframe == "Year":
                    dataset = dataset[dataset[xAxis] > matplotlib.dates.date2num(datetime.datetime.now() - datetime.timedelta(hours = 24*30*365))]
                
                global data
                data = dataset
                plt.plot_date(dataset[xAxis],dataset[yAxis],color = "r", markersize = 0,linestyle = "-",linewidth = 0.5)
                plt.tick_params(axis = "x", labelsize = 5)
                plt.title(yAxis+ " Over " +xAxis)
                plt.xlabel(xAxis)
                plt.ylabel(yAxis)
                plt.savefig(name+"/graph.png",dpi = 150)
                plt.cla()
        except Exception as error:
            print(error)
        
        st = time.time()
        while time.time() - st < 5:
            pass
        
def ClearStockData(name):
    os.remove(name+"/stockData.csv")
    print(name+ " Stock Data cleared")

tf = input("Enter a time frame(Minute/Hour/Day/Month/Year): ")
GetStockGraph("Bitcoin","Stock Price", tf)
