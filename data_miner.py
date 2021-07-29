# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 14:37:47 2021

@author: Daniel Souza - PC
"""
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import requests


URL_STATUSINVEST = 'https://statusinvest.com.br/category/advancedsearchresult?search={%22Segment%22:%22%22,%22Gestao%22:%22%22,%22my_range%22:%220;20%22,%22dy%22:{%22Item1%22:null,%22Item2%22:null},%22p_vp%22:{%22Item1%22:null,%22Item2%22:null},%22percentualcaixa%22:{%22Item1%22:null,%22Item2%22:null},%22numerocotistas%22:{%22Item1%22:null,%22Item2%22:null},%22dividend_cagr%22:{%22Item1%22:null,%22Item2%22:null},%22cota_cagr%22:{%22Item1%22:null,%22Item2%22:null},%22liquidezmediadiaria%22:{%22Item1%22:null,%22Item2%22:null},%22patrimonio%22:{%22Item1%22:null,%22Item2%22:null}}&CategoryType=2'
URL_FUNDS = 'https://www.fundsexplorer.com.br/ranking'

DATA_FOLDER = 'data/'
RAW_FILE_STATUSINVEST = 'fii_statusinvest_raw.csv'
RAW_FILE_FUNDS = 'fii_funds_raw.csv'


def get_statusinvest_data(from_web = False, url = URL_STATUSINVEST):
    if from_web:
        response = requests.get(url)
        
        print(response.status_code)
        return pd.DataFrame(response.json())
    else:
        return pd.read_csv(DATA_FOLDER + RAW_FILE_STATUSINVEST)



def get_funds_data(from_web = False, url = URL_FUNDS):
    if from_web:
        r = requests.get(url)
        doc = BeautifulSoup(r.text, 'html.parser')
        
        # Find table with data
        table = doc.find("table", {"id" : "table-ranking"})
        
        # Return DataFrame    
        return pd.read_html(str(table), header=0)[0]
    else:
        return pd.read_csv(DATA_FOLDER + RAW_FILE_FUNDS)
    

df_fe = get_funds_data()
