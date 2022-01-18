from numpy.core.fromnumeric import sort
import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go # Plotting
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import zipfile

import nltk
import string
from collections import Counter
from wordcloud import WordCloud

st.set_page_config(page_title="The Holy Quran", page_icon="🙏", layout="centered")
st.set_option('deprecation.showPyplotGlobalUse', False)
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

    df['Length'] = df['English Translation'].str.len()
    #Change Data Types
    df['Surah'] = df.Surah.astype('int')
    df['Ayah'] = df.Ayah.astype('int')
    #Merge Surah info
    df = pd.merge(df,df1,on = 'Surah',how='inner')
    return(df)
def make_data(df):
    df_1a = df.Surah.value_counts().reset_index().sort_values('index')
    df_1a = df_1a.rename(columns =\
        {'index':'Surah','Surah':'Ayah Count'})

    df_1b = df.groupby('Surah')['Length'].sum('Length').reset_index()
    df_1a = pd.merge(df_1a,df_1b, on= 'Surah', how= 'inner')
    return(df_1a)

file = get_data()
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
                st.write(file.iloc[:,:4])
            else:
                st.write(file[file['Name of Surah'] == option].iloc[:,:4])
        else:
            df_1 = file[file['Place of Revelation'] == Type]
            surahs = file[file['Place of Revelation'] == Type]['Name of Surah'].unique().tolist()
            surahs.append("All")
            surahs = np.sort(surahs)

            option = st.sidebar.selectbox("Which Surah", surahs)
            
            if option == 'All':
                st.write(df_1.iloc[:,:4])
            else:
                st.write(df_1[df_1['Name of Surah'] == option].iloc[:,:4])
elif option_select == 'Analytics':
    def surah(df):
        surahs = df['Surah'].unique().tolist()
        Surah_Data = []
        for surah in surahs:
            Data = ''
            for val in df[df["Surah"] == surah]['English Translation']:
                val1 = "  " + val
                Data += val1
            Surah_Data.append(Data)
        Surahs_df = pd.DataFrame({'Data':Surah_Data}).reset_index().rename(columns = {'index':"Surah"})
        Surahs_df['Surah']  = Surahs_df['Surah'] + 1
        df1 = pd.read_csv('Data/Surahs.csv').iloc[:,:2]

        new_df = pd.merge(Surahs_df,df1,on = 'Surah',how='inner')
        return(new_df)
    def nlp_stop():
        nltk.download("stopwords")
        nltk.download("punkt")
        #Create Stop Words Corpus
        stop_words = nltk.corpus.stopwords.words("english") + list(string.punctuation) \
        + list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) \
        + list(['--']+["''"]+["``"]+[".."]+["..."]+["ii"]+["iii"]+["iv"]+["'s"]+["the"]+["however"] \
        + ["when"]+["as"]+["meanwhile"]+['eventually'])
        return(stop_words)

    def nlp(surah_data):
        stop_words = nlp_stop()
        
        Data = ''
        for a in surah_data['Data']:
            val = "  " + a
            Data += val
        tokens = nltk.word_tokenize(Data)

        # Convert the tokens into lowercase: lower_tokens
        lower_tokens = [s.lower() for s in tokens]

        filtered_sentence  = [w for w in lower_tokens if not w in stop_words]

        #Count Words
        hr1_counter = Counter(filtered_sentence)
        df_vocab = pd.DataFrame.from_dict(hr1_counter,orient = 'index').reset_index().rename(columns = {'index':'Vocab',0:'Count'})
        df_vocab = df_vocab.sort_values('Count',ascending = False)


        return(df_vocab,hr1_counter)
    
    option_1 = st.sidebar.radio("Which Surah?",['All', 'Specific Surah'])
    surah_data = surah(file)
    
    if option_1 == 'All':
        st.markdown("## Top 10 Words in the Whole Quran")
        nn,n1 = nlp(surah_data)
        st.write(nn.head(10))

        wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(n1)
        plt.axis("off")
        plt.imshow(wordcloud)
        #plt.show()
        st.pyplot()
    else:
        option_2 = st.sidebar.selectbox("Which Surah?",sort(surah_data['Name of Surah'].unique()))
        surah_data1 = surah_data[surah_data['Name of Surah'] == option_2]
        nn,n1 = nlp(surah_data1)
        st.markdown("## Top 10 Words in {}".format(option_2))
        st.write(nn.head(10))

        wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(n1)
        plt.axis("off")
        plt.imshow(wordcloud)
        #plt.show()
        st.pyplot()