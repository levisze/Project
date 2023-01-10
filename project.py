import streamlit as st 
import math
import pandas as pd
import numpy as np
import csv
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


st.set_page_config(
    page_title="Project",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.title('Manulife MPF Data Analysis Project')
st.header ('Group 2')
st.text('Member: Eugene Erika Levi')


df = pd.read_csv("MPF_not_clean.csv")
with st.expander("Raw Dataframe"):
        st.write(df)

data = pd.read_csv("MPF_cleanned.csv")
list(data.columns.values)
for col in data.columns:
    print(col)
df = data.drop('Unnamed: 0', axis=1)
df = df.fillna(0)
with st.expander("Cleanned data"):
        st.write(df)

#chart_data = pd.DataFrame(
    #data=df,columns=['Cumulative Return: 6month','Cumulative Return: 1year',
    #'Cumulative Return: 3years','Cumulative Return: 5years']
#)
#st.line_chart(chart_data)
df.describe()
fig, ax = plt.subplots()
sns.set(font_scale=1)
sns.heatmap(df.corr(), ax=ax, annot=True)
st.write(fig)
#df.groupby(['Risk level'])






df = df.fillna(0)
df.groupby('Risk level').describe()
df.mean()












