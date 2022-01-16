import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go # Plotting
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import zipfile

st.set_page_config(page_title="The Holy Quran Analytics", page_icon="🙏", layout="centered")

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
with st.container():
    revel_list = ['Makkah','Medina','Both']
    surahs = file['Name of Surah'].unique().tolist()
    surahs.append("All")
    
    Type = option = st.selectbox("Place of Revelation", revel_list)
    if Type =='Both':
        option = st.selectbox("Which Surah", surahs)
        if option == 'All':
            st.write(file.head())
        else:
            st.write(file[file['Name of Surah'] == option].head())
    else:
        option = st.selectbox("Which Surah", file[file['Place of Revelation'] == Type]['Name of Surah'].unique())
        st.write(file[file['Name of Surah'] == option].head())