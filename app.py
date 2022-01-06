from utilsTwitterCovid import plotCovidFigure
import pandas as pd
import streamlit as st
import time
st.write("Casi Covid")
link = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"


@st.cache
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    data = pd.read_csv(url)
    return data


let = st.sidebar.slider(" ", 0.0, 0.1, 0.02)
ospDeaths = st.sidebar.slider(" ", 0.0, 0.1, 0.013)
ICUDeaths = st.sidebar.slider(" ", 0.0, 0.2, 0.115)
deathsShift = st.sidebar.slider(" ", 0, 20, 13)
hospShift = st.sidebar.slider(" ", 0, 20, 10)
ICUShift = st.sidebar.slider(" ", 0, 20, 12)
newICUshift = st.sidebar.slider(" ", 0, 20, 5)
newICUDeaths = st.sidebar.slider(" ", 0.0, 2.0, 1.7)

start = time.time()
dataCovid = fetch_and_clean_data(link)
date = dataCovid['data'].to_numpy()
lastDateString = date[-1]
caption, figureName, fig = plotCovidFigure(dataCovid,
                                           let,
                                           ospDeaths,
                                           ICUDeaths,
                                           deathsShift,
                                           hospShift,
                                           ICUShift,
                                           newICUshift,
                                           newICUDeaths)
print(time.time() - start)
st.pyplot(fig)
