import streamlit as st 
import pandas as pd
import numpy as np
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
sns.heatmap(df.corr(), ax=ax, annot=True)
st.write(fig)
#df.groupby(['Risk level'])
plt.rcParams["figure.dpi"] = 300

sns.set_theme()


def main():
    st.header("Summary")

    df = pd.read_csv("MPF_cleanned.csv")

    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[df.columns.str.startswith(' Calendar Year')], axis=1, inplace=True)
    df.dropna(inplace=True)
    df["Risk level"] = df["Risk level"].astype(int)

    # plot 1

    groups = df.groupby("Risk level").agg(["mean", "max"]).T.unstack()
    groups.index = groups.index.str.replace(r".*:\s?", "", regex=True)
    ax = groups.plot(style=["--", "-"] * 6, figsize=(9, 8))
    plt.legend(title="Risk Level")
    plt.xlabel("Period")
    plt.ylabel("Return (%)")
    plt.title("Cumulative Return across Period")
    st.pyplot(ax.get_figure())

    # plot 2
    groups = df.groupby("Risk level").agg(["mean", "max"])

    # rename columns
    legends = groups.columns.unique(level=0)
    legends = legends.str.replace(r"Cumulative Return:\s?", "", regex=True)
    groups.columns = groups.columns.set_levels(legends, level=0)

    ax = groups.plot(style=["--", "-"] * 6, figsize=(9, 8))
    plt.legend(title="Period")
    plt.ylabel("Return (%)")
    plt.title("Cumulative Return across Risk level")
    st.pyplot(ax.get_figure())


if __name__ == "__main__":
    main()





#df = df.fillna(0)
#df.groupby('Risk level').describe()
#df.mean()












