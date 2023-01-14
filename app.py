import functools
from pathlib import Path
import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report


st.set_page_config(
    page_title="Project",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.title('Manulife MPF Data Analysis Project :moneybag: :dollar: ')
st.header ('Group 2 ')
st.subheader('Member: Eugene Erika Levi')
st.text('''
    ***Data as of November 30, 2022***
''')
expander = st.subheader("Project planning:")
st.markdown('''
    **:red[About Manulife:]**
    \n:blue[Manulife is the No.1 MPF service provider in Hong Kong, according to the Mercer MPF Market Shares Report.
    Also they are No.1 in MPF market share, around 27%. ]
 ''')   
st.markdown(''' 
    **:red[Questions:]**
    \n:blue[-What data can we get from the website?]
    \n:blue[-Is possibility of scrapping the website?]
    \n:blue[-What data must be analysing?]
''')
st.markdown('''
    **:red[Data Collection:]**
    \n:blue[Scraping Manulife MPF Website (Constituent Fund, Cumulative Return, Risk Level)]
''')
st.markdown('''
    **:red[Data Cleaning & transformation:]**
    \n:blue[Remove the unrelated data, transform the data in efficient format.]
''')
st.markdown('''
    **:red[Data Visualization:]**
    \n:blue[1.Cumulative Return across Period.]
    \n:blue[2.Cumulative Return across Risk level.]
    \n:blue[3.Best Cumulative Return across Period.]
''')


data0 = pd.read_csv("MPF_not_clean.csv")
with st.expander("Raw Dataframe"):
        st.write(data0)

data = pd.read_csv("MPF_cleanned.csv")
list(data.columns.values)
for col in data.columns:
    print(col)
df = data.fillna(0)
with st.expander("Cleanned data"):
    st.write(df)    
    
data1 = pd.read_csv("MPF_cleanned.csv")     
pr = data1.profile_report()
df1 = data1.fillna(0)
with st.expander("Report",expanded=True):
    st_profile_report(pr) 



def main():
    st.header("Analysis")

    data2 = pd.read_csv("MPF_cleanned.csv")

    data2.drop(columns=data2.columns[0], axis=1, inplace=True)
    data2.drop(columns=data2.columns[data2.columns.str.startswith(' Calendar Year')], axis=1, inplace=True)
    data2.dropna(inplace=True)
    data2["Risk level"] = data2["Risk level"].astype(int)

    # plot 1

    groups = data2.groupby("Risk level").agg(["mean", "max"]).T.unstack()
    groups.index = groups.index.str.replace(r".*:\s?", "", regex=True)
    ax = groups.plot(style=["--", "-"] * 6, figsize=(9, 8))
    plt.legend(title="Risk Level")
    plt.xlabel("Period")
    plt.ylabel("Return (%)")
    plt.title("Cumulative Return across Period")
    st.pyplot(ax.get_figure())

    st.markdown('''
     **Under current market condition, different asset classes are affected in different ways
     and to a different extant. Apart from risk 5 return, given to others risk level products return in 6 month to 5 years
     fell behind 0.**
 ''')   
    st.markdown('''
    **High risk products have a bad started but the return will grow with the increase of time.
    Given to all risk level products, Risk 5 have the best return comparing to others.**
''')

    # plot 2
    groups = data2.groupby("Risk level").agg(["mean", "max"])

    # rename columns
    legends = groups.columns.unique(level=0)
    legends = legends.str.replace(r"Cumulative Return:\s?", "", regex=True)
    groups.columns = groups.columns.set_levels(legends, level=0)

    ax = groups.plot(style=["--", "-"] * 6, figsize=(9, 8))
    plt.legend(title="Period")
    plt.ylabel("Return (%)")
    plt.title("Cumulative Return across Risk level")
    st.pyplot(ax.get_figure())

    st.markdown('''
    **Returns of less than 1 year investment were fell when the risk level was getting higher and higher.**   
''')
    st.markdown('''
    **Given to all risk level products, Risk 5 investments are positive when more than 3years.**
''')
    #plot 3
    a1 = df[['Cumulative Return: 6month','Constituent Fund']].sort_values(by='Cumulative Return: 6month',ascending=False)[0:30]
    a1['Period'] = '6month'
    a1 = a1.reset_index()
    a1 = a1.drop(['index'],axis=1)
    a1 = a1.rename(columns={'Cumulative Return: 6month': 'Return',})


    a2 = df[['Cumulative Return: 1year','Constituent Fund']].sort_values(by='Cumulative Return: 1year',ascending=False)[0:30]
    a2['Period'] = '1year'
    a2 = a2.reset_index()
    a2 = a2.drop(['index'],axis=1)
    a2 = a2.rename(columns={'Cumulative Return: 1year': 'Return'})


    a3 = df[['Cumulative Return: 3years','Constituent Fund']].sort_values(by='Cumulative Return: 3years',ascending=False)[0:30]
    a3['Period'] = '3years'
    a3 = a3.reset_index()
    a3 = a3.drop(['index'],axis=1)
    a3 = a3.rename(columns={'Cumulative Return: 3years': 'Return'})


    a4 = df[['Cumulative Return:5years','Constituent Fund']].sort_values(by='Cumulative Return:5years',ascending=False)[0:30]
    a4['Period'] = '5years'
    a4 = a4.reset_index()
    a4 = a4.drop(['index'],axis=1)
    a4 = a4.rename(columns={'Cumulative Return:5years': 'Return'})


    total = pd.concat([a1,a2,a3,a4])
    total = total.reset_index()
    total = total.drop(['index'],axis=1)
    total = total.rename(columns={'Constituent Fund': 'Fund'})


    plt.figure(figsize=(10,10))
    ax = sns.scatterplot(x = total.Period, y = total.Return, hue = total.Fund, s = 100)
    plt.legend(bbox_to_anchor=(1.05, 1),title='Constituent Fund')
    plt.title("Best Cumulative Return across Period",fontsize = 20)
    plt.xlabel("Period")
    plt.ylabel("Return (%)")
    plt.savefig("Best Cumulative Return across Period", bbox_inches='tight')
    st.pyplot(ax.get_figure())

    st.markdown('''
    **Best 3 of 6 month investment: 1.Healthcare Fund 2.Conservative Fund 3.Interest Fund**
''')
    st.markdown('''
    **Best 3 of 1 year investment: 1.International Bond Fund 2.Healthcare Fund 3.Interest Fund**
''')
    st.markdown('''
    **Best 3 of 3 year investment: 1.Healthcare Fund 2.North American Equity Fund 3.European Equity Fund**
''')
    st.markdown('''
    **Best 3 of 5 year investment: 1.Healthcare Fund 2.North American Equity Fund 3.European Equity Fund**
''')

    st.header('Conclusion')
    st.markdown('''
    **As we already know, collecting data on Constituent Fund, Cumulative Return, Risk Level has allowed current customers or 
    potential customers to empower with knowledge about Manulife MPF service.**
''')
    st.markdown('''
    **Healthcare Fund had a best return in 6month, 3year, and 5year investment. It maybe affected by Covid-19. Also, NA & EU Equity Fund
    had a great return in long-term. But we can see that Hang Seng Index Tracking Fund, HK Equity Fund, and chia value fund had a
    bad return in short-term & long-term. It maybe affected by china & HK poilcy.**
''')
    st.subheader('Price volatility')
    st.markdown('''
    **Market volatility maybe of concern to anxious investors whose focus is on the short-term. However, for 
    longer-term investors who invest for retirement in the MPF, market fluctuation along the way are inevitable.**    
''')










if __name__ == "__main__":
    main()













