from utils import plotCovidFigure
import pandas as pd
import streamlit as st
import numpy as np
import datetime

@st.cache(ttl=3600)
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    data = pd.read_csv(url)
    return data

def app():
    st.write("## Analisi Dati Covid Protezione Civile") #markdown

    st.write("I dati contengono i nuovi casi, nuovi decessi,"
        " nuove terapie intensive, terapie intensive occupate "
        "e posti letto occupati notificati giorno per giorno.") #markdown
    st.write("Qui sotto tracciamo tutti i dati in media mobile a 7 giorni: "
    "ogni dato rappresenta la media dei 7 giorni precedenti. Tutte le linee sono raffigurate in un'immagine sola e si "
        "possono cambiare alcuni parametri per le varie curve: "
        "un coefficiente che alza e abbassa le curve e uno "
        "shift di giorni rispetto alla notifica. Prova a variarli nella barra laterale!")
    st.write("Interessante è vedere come le curve possano sovrapporsi "
        "per alcune fasi della pandemia se i coefficienti sono scelti bene.")
    st.write("Al variare delle fasi della pandemia si nota come "
        "le relazioni tra le curve si modifichino e questo grafico **aiuti a capire** come si evolve la pandemia.")
    link = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

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

    #startDate = st.sidebar.date_input('Data iniziale', min_value=dateValues[0], max_value=dateValues[-1], value=datetime.date(2020,8,15))
    #endDate = st.sidebar.date_input('Data Finale', min_value=dateValues[0], max_value=dateValues[-1]+ datetime.timedelta(days=10), value=dateValues[-1]+ datetime.timedelta(days=10))
    logScale = st.sidebar.checkbox("Scala logaritmica",value=True)
    let = st.sidebar.slider("Letalità", 0.0, 0.03, 0.02,step=0.001,format="%1.3f")
    ospCases = st.sidebar.slider("Ospedalizzati su nuovi casi", 0.0, 2.0, 0.02/0.013,step=0.01)
    ICUCases = st.sidebar.slider("Terapie intensive su nuovi casi", 0.0, 0.2, 0.02/0.115,step=0.001,format="%1.3f")
    newICUCases = st.sidebar.slider("Nuove terapie intensive su nuovi casi", 0.0, 0.015, 0.02/1.7,step=0.0001,format="%1.4f")
    deathsShift = st.sidebar.slider("Ritardo dei decessi", 0, 20, 13)
    hospShift = st.sidebar.slider("Ritardo delle ospedalizzazioni", 0, 20, 10)
    ICUShift = st.sidebar.slider("Ritardo delle terapie intensive", 0, 20, 12)
    newICUshift = st.sidebar.slider("Ritardo delle nuove terapie intensive", 0, 20, 5)

    #caption, fig, fig2 = 
    plotCovidFigure(
        nuovi_decessi_average, nuovi_positivi_average, nuovi_TI_average, TI, ospedalizzati, dateValues,
                                               #endDate,
                                               #startDate,
                                               let,
                                               ospCases,
                                               ICUCases,
                                               newICUCases,
                                               deathsShift,
                                               hospShift ,
                                               ICUShift , 
                                               newICUshift,
                                               logScale)
#    st.pyplot(fig)
#    st.pyplot(fig2)

    st.write("Qua sopra sono raffigurati "
        "i rapporti tra i nuovi decessi e i nuovi casi "
        "e tra le nuove terapie intensive e i nuovi casi. "
        "Anche in questo caso i decessi e le terapie intensive "
        "sono shiftate dei giorni settati. Questo è necessario per"
        " tener conto del ritardo che c'è tra la notifica del caso"
        " e del decesso o del ricovero in terapia intensiva.")
    st.write("Questo grafico ci racconta approsimativamente "
        "come si è modificata la letalità appartente e "
        "il tasso di ricovero in terapia intensiva.")
    st.markdown("""Queste quantità dipendono da tanti fattori: 
        * la letalità dipende dalle fasce d'età e in fasi diverse
                 diverse della pandemia, diverse fasce d'età son state colpite
        * il denominatore (i casi notificati) è fortemente influenzato dal testing
        * grossi eventi superspreading possono modificare di molto numeratore e denominatore
        a seconda delle categorie esposte agli eventi
        * festività possono cambiare i network di contatti
        * tanti altri ancora 
""")
    st.write("Quindi questi risultati vanno presi con cautela "
        "e usati solo per avere un'idea generale dell'andamento in tempi rapidi. "
        "Per risultati più precisi è meglio usare i dati per fasce d'età rilasciati "
        "dall'Istituto superiore della sanità [a questo link](https://www.epicentro.iss.it/coronavirus/)")

    st.write("Dati disponibili giornalmente su "
        "[github](https://github.com/pcm-dpc/COVID-19) "
        "pubblicati dalla protezione civile")


