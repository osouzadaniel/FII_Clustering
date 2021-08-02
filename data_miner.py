# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 14:37:47 2021

@author: Daniel Souza
"""
from bs4 import BeautifulSoup
import pandas as pd
import requests

class DataFII():
    URL_STATUSINVEST = 'https://statusinvest.com.br/category/advancedsearchresult?search={%22Segment%22:%22%22,%22Gestao%22:%22%22,%22my_range%22:%220;20%22,%22dy%22:{%22Item1%22:null,%22Item2%22:null},%22p_vp%22:{%22Item1%22:null,%22Item2%22:null},%22percentualcaixa%22:{%22Item1%22:null,%22Item2%22:null},%22numerocotistas%22:{%22Item1%22:null,%22Item2%22:null},%22dividend_cagr%22:{%22Item1%22:null,%22Item2%22:null},%22cota_cagr%22:{%22Item1%22:null,%22Item2%22:null},%22liquidezmediadiaria%22:{%22Item1%22:null,%22Item2%22:null},%22patrimonio%22:{%22Item1%22:null,%22Item2%22:null}}&CategoryType=2'
    URL_FUNDS = 'https://www.fundsexplorer.com.br/ranking'
    
    DATA_FOLDER = 'data/'
    RAW_FILE_STATUSINVEST = 'fii_statusinvest_raw.csv'
    RAW_FILE_FUNDS = 'fii_funds_raw.csv'
    
    def __init__(self):
        pass
    
    
    def get_raw_data_statusinvest(self, from_web = False, url = URL_STATUSINVEST):
        if from_web:
            response = requests.get(url)
            
            return pd.DataFrame(response.json())
        else:
            return pd.read_csv(self.DATA_FOLDER + self.RAW_FILE_STATUSINVEST, sep = ';')
    
    
    
    def get_raw_data_fundsexplorer(self, from_web = False, url = URL_FUNDS):
        if from_web:
            r = requests.get(url)
            doc = BeautifulSoup(r.text, 'html.parser')
            
            # Find table with data
            table = doc.find("table", {"id" : "table-ranking"})
            
            # Return DataFrame    
            return pd.read_html(str(table), header=0)[0]
        else:
            return pd.read_csv(self.DATA_FOLDER + self.RAW_FILE_FUNDS, sep = ';')
        
    
    def get_processed_data_fundsexplorer(self):
        f_str_to_num = lambda x: pd.to_numeric(x.replace('R$ ','').replace('%','').replace('.','').replace(',','.'))
        
        df_fe = pd.read_csv(self.DATA_FOLDER + self.RAW_FILE_FUNDS, sep = ';',
                            converters = {'Preço Atual':f_str_to_num, 
                                          'Dividendo':f_str_to_num,
                                          'DividendYield':f_str_to_num,
                                          'DY (3M)Acumulado':f_str_to_num,
                                          'DY (6M)Acumulado':f_str_to_num,
                                          'DY (12M)Acumulado':f_str_to_num,
                                          'DY (3M)Média':f_str_to_num,
                                          'DY (6M)Média':f_str_to_num,
                                          'DY (12M)Média':f_str_to_num,
                                          'DY Ano':f_str_to_num,
                                          'Variação Preço':f_str_to_num,
                                          'Rentab.Período':f_str_to_num,
                                          'Rentab.Acumulada':f_str_to_num,
                                          'PatrimônioLíq.':f_str_to_num,
                                          'VPA':f_str_to_num,
                                          'DYPatrimonial':f_str_to_num,
                                          'VariaçãoPatrimonial':f_str_to_num,
                                          'Rentab. Patr.no Período':f_str_to_num,
                                          'Rentab. Patr.Acumulada':f_str_to_num,
                                          'VacânciaFísica':f_str_to_num,
                                          'VacânciaFinanceira':f_str_to_num},
                            dtype = {'Liquidez Diária' : float})
        
        # Drop the first unnamed column
        df_fe.drop("Unnamed: 0", axis = 1, inplace=True)
        
        # Rename columns
        df_fe.columns = ['ticker', 'setor', 'preço', 'num_negocios', 'div_mes_brl', 'dy_1m', 'dy_3m_acc', 'dy_6m_acc', 'dy_12m_acc',
                         'dy_3m_avg', 'dy_6m_avg', 'dy_12m_avg', 'dy_ano', 'var_preço', 'rent_periodo', 'rent_acc', 'PL', 'VPA', 'PVPA',
                         'dy_VPA', 'var_VPA', 'rent_VPA_periodo', 'rent_VPA_acc', 'vacancia_fisica', 'vacancia_financeira', 'qtd_ativos']
        
        return df_fe
    
    def get_processed_data_statusinvest(self):
        df_si = pd.read_csv(self.DATA_FOLDER + self.RAW_FILE_STATUSINVEST, sep = ';')
        df_si.drop(["Unnamed: 0", "companyId"], axis = 1, inplace = True)
        
        # Rename columns
        df_si.columns = ['nome', 'ticker', 'preço', 'tipo_gestao', 'dy', 'pct_caixa', 'num_cotistas', 'PL', 'PVPA', 'liquidez_diaria_avg',
                         'cagr_dividendo', 'cagr_cota']
        
        return df_si
    
    def update_FII_data_from_web(self):
        print("Obtendo dados de Funds Explorer...")
        df_fe = self.get_raw_data_fundsexplorer(from_web=True)
        print('... ok')
        
        print("Obtendo dados de Status Invest...")
        df_si = self.get_raw_data_statusinvest(from_web=True)
        print('... ok')
        
        # Save .csv files
        df_fe.to_csv(self.DATA_FOLDER + self.RAW_FILE_FUNDS, sep = ';', index = False)
        df_si.to_csv(self.DATA_FOLDER + self.RAW_FILE_STATUSINVEST, sep = ';', index = False)
        
    
    def get_FII_data(self):
        df_fe = self.get_processed_data_fundsexplorer()
        df_si = self.get_processed_data_statusinvest()
        
        # Remove duplicated data
        df_fe.drop(['preço', 'PL', 'PVPA'], axis = 1, inplace = True)
        
        # Merge dataframes on same ticker    
        df = pd.merge(df_si, df_fe, left_on="ticker", right_on="ticker", how = 'outer')
        
        # Reorder columns - leave categorical data first
        col_names = list(df.columns)
        col_names_cat = ['ticker', 'nome', 'tipo_gestao', 'setor']
        col_names_cat.reverse()
        
        for col in col_names_cat:
            col_names.remove(col)
            col_names.insert(0, col)
        
        df = df.reindex(columns=col_names)
        
        return df

