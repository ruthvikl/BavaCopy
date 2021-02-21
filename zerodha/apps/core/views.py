from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponse
from io import BytesIO
from django.shortcuts import redirect
from urllib.request import urlopen, Request
from datetime import datetime, date, timedelta 
from zipfile import ZipFile
from bs4 import BeautifulSoup 
import csv
import requests
import urllib
import pytz
import pandas as pd
import zipfile
import json
import os
# Create your views here.

def tablepage(request):
    tz = pytz.timezone('Asia/Kolkata')
    dt = datetime.now(tz)
    dayofweek = datetime.today().strftime("%A")
    now = dt.strftime("%H")  # geting time of the day 
    today = date.today()
    if dayofweek == "Sunday":
        today = today - timedelta(days = 2)
    elif now < "18" or dayofweek == "Saturday":
        today = today - timedelta(days = 1)
    d3 = today.strftime("%d%m%y") # time object to get date 
    a = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"+ d3 +"_CSV.ZIP"
    b = "EQ" + d3 + "_CSV.ZIP"
    c = "EQ" + d3 + ".CSV"
    d = Request(a, headers={'User-Agent': 'Mozilla/5.0'})
    download = urllib.request.urlopen(d)
    with open(os.path.basename(a), "wb") as f:
        f.write(download.read())

    today = date.today()
    zf = zipfile.ZipFile(b) 
    df = pd.read_csv(zf.open(c))
    json_records = df.reset_index().to_json(orient ='records') 
    data = [] 
    data = json.loads(json_records) 
    context = {'user': data} 
    return render(request, 'tablepage.html', context)
    
def writetocsv(request):
    path = urlopen("http://127.0.0.1:8000/")
    data = [] 
   
    # for getting the header from 
    # the HTML file 
    list_header = [] 
    soup = BeautifulSoup(path,'html.parser') 
   
    header = soup.find_all("table")[0].find("tr") 
    
    for items in header: 
        try: 
            list_header.append(items.get_text()) 
        except: 
            continue
    
    # for getting the data  
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:] 
    
    for element in HTML_data: 
        sub_data = [] 
        for sub_element in element: 
            try: 
                sub_data.append(sub_element.get_text()) 
            except: 
                continue
        data.append(sub_data) 
    
    # Storing the data into Pandas 
    # DataFrame  
    dataFrame = pd.DataFrame(data = data, columns = list_header) 
    download_folder = os.path.expanduser("~")+"/Downloads/Bavacopy.csv"
    dataFrame.to_csv(download_folder,index = False, header=True)
    return redirect(tablepage)
      
