from utilsTwitterCovid import plotCovidFigure
import pandas as pd
import streamlit as st
import time
import numpy as np
import datetime

st.write("Casi Covid") #markdown
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

ospedalizzati = dataCovid['totale_ospedalizzati'].to_numpy()
nuovi_positivi = dataCovid['nuovi_positivi'].to_numpy()
maxLen = len(nuovi_positivi)

decessiTotali = dataCovid['deceduti'].to_numpy()
nuovi_decessi = np.zeros(maxLen)
nuovi_decessi[1:] = decessiTotali[1:] - decessiTotali[:-1]
nuovi_TI = dataCovid['ingressi_terapia_intensiva'].to_numpy()
TI = dataCovid['terapia_intensiva'].to_numpy()
nuovi_decessi_average = np.zeros(maxLen)
nuovi_decessi_average[6:] = np.convolve(nuovi_decessi, 1 / 7 * np.ones(7), 'valid')
nuovi_positivi_average = np.zeros(maxLen)
nuovi_positivi_average[6:] = np.convolve(nuovi_positivi, 1 / 7 * np.ones(7), 'valid')
nuovi_TI_average = np.zeros(maxLen)
nuovi_TI_average[6:] = np.convolve(nuovi_TI, 1 / 7 * np.ones(7), 'valid')
dates = dataCovid['data'].to_numpy()
dateValues = [datetime.datetime.strptime(dates[d][:10], "%Y-%m-%d").date() for d in range(maxLen)]

caption, figureName, fig = plotCovidFigure(
    nuovi_decessi_average, nuovi_positivi_average, nuovi_TI_average, TI, ospedalizzati, dateValues,
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
