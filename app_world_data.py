import pandas as pd
import streamlit as st
import time
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


@st.cache
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    data = pd.read_csv(url)
    return data


def app():
    link = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    st.write("# Analisi Dati Covid Mondo")  # markdown
    st.write(
        "Dati disponibili *giornalmente* su [Our World in Data](https://covid.ourworldindata.org)"
        " su nuovi casi, nuovi decessi. **Attenzione!** "
        "Non tutte le nazioni usano le stesse definizioni, quindi i paragoni "
        "tra nazioni diverse non sono troppo attendibili.")  # markdown
    st.write("Qui sotto tracciamo i dati in media mobile a 7 giorni: "
    "ogni dato rappresenta la media dei 7 giorni precedenti") #markdown
    st.write("Le linee sono raffigurate in un'immagine sola e si "
        "possono cambiare alcuni parametri per le varie curve: "
        "un coefficiente che alza e abbassa i decessi (la letalità apparente) e uno "
        "shift di giorni rispetto alla notifica. Prova a variarli nella barra laterale!")
    st.write("Interessante è vedere come le curve possano sovrapporsi "
        "per alcune fasi della pandemia se i coefficienti sono scelti bene.")
    st.write("Al variare delle fasi della pandemia si nota come "
        "le relazioni tra le curve si modifichino e questo grafico"
        " aiuta a capire come si evolve la pandemia.")

    dataCovid = fetch_and_clean_data(link)

    country = st.sidebar.selectbox("Nazione", dataCovid.location.unique(), index=104)
    startDate = st.sidebar.date_input('Data iniziale', min_value=datetime.date(2020, 3, 1),
                                      max_value=datetime.datetime.today(), value=datetime.date(2020, 3, 1))
    endDate = st.sidebar.date_input('Data Finale', min_value=datetime.date(2020, 3, 1),
                                    max_value=datetime.datetime.today() + datetime.timedelta(days=10),
                                    value=datetime.datetime.today() + datetime.timedelta(days=10))
    logScale = st.sidebar.checkbox("Scala logaritmica", value=True)
    let = st.sidebar.slider("Letalità", 0.0, 0.1, 0.02, step=0.001, format="%1.3f")
    deathsShift = st.sidebar.slider("Ritardo dei decessi", 1, 20, 13)

    fig, fig2 = plotCovidData(dataCovid, country, startDate, endDate, fatality=let, deathDelay=deathsShift,
                              logScale=logScale)

    st.pyplot(fig)
    st.pyplot(fig2)

    st.write("Qua sopra sono raffigurati "
        "i rapporti tra i nuovi decessi e i nuovi casi."
        "Anche in questo caso i decessi "
        "sono shiftati dei giorni settati. Questo è necessario per"
        " tener conto del ritardo che c'è tra la notifica del caso"
        " e del decesso.")
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
* tanti altri ancora.
""")
    st.write("Quindi questi risultati vanno presi con cautela "
        "e usati solo per avere un'idea generale dell'andamento in tempi rapidi. "
        "Per risultati più precisi è meglio usare i dati per fasce d'età: non tutti le nazioni li rilasciano.")



def plotCovidData(dataCovid, country, startDate, endDate, fatality=2, deathDelay=12, logScale=True):
    mask = dataCovid.location == country
    countryCovidData = dataCovid.loc[mask]
    pop100 = countryCovidData.population.iloc[0] / 100000

    nuoviDecAveraged = np.convolve(countryCovidData['new_deaths'].to_numpy(), 1 / 7 * np.ones(7), 'valid') / pop100;
    nuoviCasAveraged = np.convolve(countryCovidData['new_cases'].to_numpy(), 1 / 7 * np.ones(7), 'valid') / pop100;
    idxsNan = np.isnan(nuoviDecAveraged)
    nuoviDecAveraged[idxsNan] = 0
    idxsNan = np.isnan(nuoviCasAveraged)
    nuoviCasAveraged[idxsNan] = 0

    dates = countryCovidData['date'].to_numpy()
    ll = len(nuoviDecAveraged)
    lenDates = len(dates)
    dateValuesCases = [datetime.datetime.strptime(dates[d], "%Y-%m-%d").date() for d in range(lenDates - ll, lenDates)]
    dateValuesDeaths = [k + datetime.timedelta(days=-deathDelay) for k in dateValuesCases]
    formatter = mdates.DateFormatter("%m-%Y")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    maxPlots = max(max(nuoviCasAveraged), max(nuoviDecAveraged / fatality)) * 1.2
    minPlots = min(min(nuoviCasAveraged[100:]), min(nuoviDecAveraged[100:] / fatality)) * 0.8

    color = 'tab:blue'

    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('New Cases per 100 000 population (7 days average)', color=color)
    if not logScale:
        ax1.plot(dateValuesCases, nuoviCasAveraged, label="Cases", color=color)
    else:
        ax1.semilogy(dateValuesCases, nuoviCasAveraged, label="Cases", color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    xticks = []
    for yy in range(2020, 2023):
        for d in range(1, 13, 2):
            xticks.append(datetime.date(yy, d, 1))
    ax1.set_xticks(xticks)
    ax1.set_ylim([max(minPlots, 10 ** -3), maxPlots])
    ax1.set_xlim([startDate, endDate])
    ax1.grid(True)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.xaxis.set_major_formatter(formatter)
    ax2.set_ylabel('New Deaths per 100 000 population (7 days average)',
                   color=color)  # we already handled the x-label with ax1
    if not logScale:
        ax2.plot(dateValuesDeaths, nuoviDecAveraged, color=color)
    else:
        ax2.semilogy(dateValuesDeaths, nuoviDecAveraged, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xticks(xticks)
    ax2.set_ylim([max(minPlots, 10 ** -3) * fatality, maxPlots * fatality])
    ax2.set_xlim([startDate, endDate])

    plt.title(country)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    fig2, ax5 = plt.subplots(1, 1, figsize=(10, 6))
    plt.plot(dateValuesCases[deathDelay:], nuoviDecAveraged[deathDelay:] / nuoviCasAveraged[:-deathDelay])
    ax5.xaxis.set_major_formatter(formatter)
    ax5.set_xlabel('Date')
    plt.ylim([0, 0.05])
    ax5.set_xticks(xticks)
    yticks = np.linspace(0, 0.05, 11)
    ax5.set_yticks(yticks)
    ax5.set_ylabel("Frazione decessi su casi")
    plt.xlim([startDate, endDate])
    plt.grid(True)
    plt.title("Letalità apparente")
    return fig, fig2
