import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go # Plotting
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import zipfile

st.set_page_config(page_title="The Holy Quran", page_icon="🙏", layout="centered")

st.title("🙏 The Holy Quran")
@st.cache 
def get_data():
    #Read df
    df = pd.read_csv('Data/en.ahmedali.txt',\
        delimiter="|",header=None)
    df1 = pd.read_csv('Data/Surahs.csv')
    #Rename Columns
    df = df.rename(columns =\
        {0:'Surah',1:'Ayah',2:'English Translation'})
    
    #Remove Credit info
    df = df.iloc[:-11,:]
    #Change Data Types
    df['Surah'] = df.Surah.astype('int')
    df['Ayah'] = df.Ayah.astype('int')
    #Merge Surah info
    df = pd.merge(df,df1,on = 'Surah',how='inner')
    return(df)
file = get_data()

def make_data(df):
    df_1a = df.Surah.value_counts().reset_index().sort_values('index')

    return(df_1a)
df = make_data(file)

Options = ['Reader','Analytics']
option_select = st.sidebar.\
    selectbox("What would you like?",Options)

if option_select == 'Reader':
    revel_list = ['Makkah','Medina','Both']
    surahs = file['Name of Surah'].\
        unique().tolist()
    surahs.append("All")
    surahs = np.sort(surahs)
    Type = st.sidebar.\
        selectbox("Place of Revelation", revel_list, index = revel_list.index('Both'))

    with st.container():
        if Type =='Both':
            option = st.sidebar.selectbox("Which Surah", surahs)
            if option == 'All':
                st.write(file.iloc[:,:3])
            else:
                st.write(file[file['Name of Surah'] == option].iloc[:,:3])
        else:
            df_1 = file[file['Place of Revelation'] == Type]
            surahs = file[file['Place of Revelation'] == Type]['Name of Surah'].unique().tolist()
            surahs.append("All")
            surahs = np.sort(surahs)

            option = st.sidebar.selectbox("Which Surah", surahs)
            
            if option == 'All':
                st.write(df_1.iloc[:,:3])
            else:
                st.write(df_1[df_1['Name of Surah'] == option].iloc[:,:3])