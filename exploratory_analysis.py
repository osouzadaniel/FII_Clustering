# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 15:31:47 2021

@author: Daniel Souza - PC
"""
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from pandas.api.types import is_numeric_dtype

def plot_histograms(df, title, n_columns = 4):
    fig_columns = n_columns
    fig_rows = int(np.ceil(len(df.columns) / fig_columns))
    
    fig, axes = plt.subplots(fig_rows, fig_columns, figsize=(18, 4 * fig_rows))
    fig.suptitle(title, size='xx-large')

    for i, column in enumerate(df.columns):
        ax = axes[i//fig_columns][i%fig_columns]
        
        sns.histplot(data = df, x = column, ax=ax, kde = True)
        
        if(is_numeric_dtype(df[column])):
            ax.axvline(x=np.mean(df[column]), linestyle='dashed', label='Mean')
            ax.legend()
        

        ax.set_title(column.title().replace("_", " "))
        

    plt.tight_layout()
    
    return fig

def plot_high_correlation_variables(df, correlation, correl_threshold, title, n_columns = 4):
    fig_columns = 4

    high_corr_pair_list = []
    
    # Add high correlation variables pairs to list
    for i, line in enumerate(correlation.columns):
        for column in correlation.columns[i+1:]:
            cor_abs_val = np.abs(correlation.loc[line, column])
            
            if cor_abs_val >= correl_threshold:
                high_corr_pair_list.append([line, column, cor_abs_val])
    
    # Sort list according to absolute correlation
    high_corr_pair_list.sort(reverse = True, key = lambda x: x[2])
    # Set amount of rows            
    fig_rows = int(np.ceil(len(high_corr_pair_list) / fig_columns))
    
    # Plot charts
    fig, axes = plt.subplots(fig_rows, fig_columns, figsize=(18, 4*fig_rows))
    fig.suptitle(title, size='xx-large')
    
    for i, pair in enumerate(high_corr_pair_list):
        if fig_rows > 1:
            ax = axes[i//fig_columns][i%fig_columns]
        else:
            ax = axes[i]
            
        cor_i = correlation.loc[pair[0], pair[1]]
        
        sns.scatterplot(data = df, x = pair[1], y = pair[0], ax = ax, alpha = 0.8)
        ax.set_title(str(pair[0]).title().replace("_", " ") + " x " + str(pair[1]).title().replace("_", " ") \
                     + ", corr = {:.2f}".format(cor_i) )
        
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    return fig