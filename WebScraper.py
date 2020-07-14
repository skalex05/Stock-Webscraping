import requests, os ,csv, matplotlib
from datetime import datetime as dt
from csv import writer
from bs4 import BeautifulSoup



def filterValue(string):
    st = ""
    for char in string:
        if not char in ["(",")","%",","]:
            st += char
        
    return st

def ShowStockData(name,htmlLink,spanIndex):
    if not os.path.isfile(name+"/stockData.csv"):
        try:
            os.mkdir(name)
        except Exception:
            pass
        with open(name+"/stockData.csv", 'w+',newline = "") as csvfile:
             wr = writer(csvfile, quoting=csv.QUOTE_ALL)
             wr.writerow(["DateTime","Stock Price","Average Difference","Percentage Difference"])
    with open(name+"/index.html","w+") as htmlpage:
        htmlpage.write("""<DOCTYPE html>
<html lang = 'en)'>
<head>
  <meta http-equiv="refresh" content = '5'>
  <meta charset - 'UTF-8'>
  <title>"""+name+""" Web Scraper</title>
</head>
<body>
  <h1>"""+name+""" Web Scraper!</h1>
  <img src = 'graph.png'>
</body>
</html>
""")
    
    
    try:
        response = requests.get(htmlLink)
    except Exception as err:
        print(err)
        return None
    htmlDoc = response.text

    accessed = False
    attempts = 0
    maxattempts = 5
    while not accessed:
        if attempts >= maxattempts:
            print("Failed to access html")
            return None
        try:
            soup = BeautifulSoup(htmlDoc,"html.parser")
            divs = soup.find_all("div",{"id":"app"})[0]     
            spans = divs.find_all("span")
            accessed = True
        except Exception:
            attempts += 1
            pass

    #----------------------Debug---------------------------------------------------
    
    stockPrice = filterValue(spans[spanIndex].text)
    belowAverage = filterValue(spans[spanIndex+1].text.split()[0])
    percentagefromAverage = filterValue(spans[spanIndex+1].text.split()[1])
    dateTime = str(dt.now()).split(".")[0]
    
    print("----------------------------------------------------------------------")
    print(name+":")
    print("Stock Price: "+ stockPrice)
    print("Difference to average price: "+ belowAverage)
    print("Percentage Difference to average price: " + percentagefromAverage)
    print(dateTime)
    try:
        with open(name+"/stockData.csv", 'a',newline = "") as csvfile:
             wr = writer(csvfile, quoting=csv.QUOTE_ALL)
             wr.writerow([matplotlib.dates.date2num(dt.strptime(dateTime,"%Y-%m-%d %H:%M:%S")),float(stockPrice),float(belowAverage),float(percentagefromAverage)])
             csvfile.close()
    except Exception as exception:
        print(exception)
        return None
    return stockPrice