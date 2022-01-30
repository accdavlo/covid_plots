from utils import plotCovidFigure
import pandas as pd
import streamlit as st
import numpy as np
import datetime
import altair as alt
from scipy.stats import gamma 

@st.cache(ttl=3600)
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    data = pd.read_csv(url)
    return data

def app():
    st.write("# Confronto casi convoluti con decessi") #markdown
    st.write("""
        In questa pagina cerchiamo di migliorare la mera sovrapposizione dei casi e decessi
        con uno shift di qualche giorno. In particolare, grazie ai [dati dell'istituto superiore della sanità](https://www.epicentro.iss.it/coronavirus/sars-cov-2-sorveglianza-dati)
        possiamo descrivere in maniera più precisa quanto tempo passa in media dalla diagnosi al decesso.

        Supponendo che il tempo che trascorre tra la positività di un paziente e il decesso per COVID-19 
        si distribuisca come una [Gamma](https://it.wikipedia.org/wiki/Distribuzione_Gamma), possiamo stimare
        i parametri di questa probabilità usando i dati precenti.
        Usando i dati delle varianti originale e alpha, otteniamo una distribuzione con shape=2.11 e scale=6.71.
        Se la rappresentiamo, vediamo come si distribuiscono i decessi nei giorni successivi alla positività.
    """)
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
    #logScale = st.sidebar.checkbox("Scala logaritmica",value=True)
    let = st.sidebar.slider("Letalità", 0.0, 0.03, 0.02,step=0.0005,format="%1.4f")
    shape = st.sidebar.slider(r"Shape della Gamma", 1.0, 5.0, 2.11,step=0.01,format="%1.2f")
    scale = st.sidebar.slider(r"Scale della Gamma", 0.0, 12., 6.71,step=0.01,format="%1.2f")

    Tmax=100
    xx=np.linspace(0,Tmax,Tmax+1)
    pdfGamma=gamma.pdf(xx,shape,scale=scale)
    pdfGamma=pdfGamma/sum(pdfGamma)
    media = scale*shape

    print(dateValues[-1]+datetime.timedelta(days=3))
    dateValuesConvolution=dateValues.copy()
    print(dateValuesConvolution)
    for k in range(1,Tmax):
        dateValuesConvolution.append(
        dateValues[-1]+datetime.timedelta(days=k)
        )

    casi_convoluti = np.convolve(nuovi_positivi_average,pdfGamma)

    gammaDist = pd.DataFrame({
            'Giorni':xx,
            'Distribuzione dei decessi': pdfGamma,
            'media':media
    })


    multi = alt.selection_multi(on='mouseover', nearest=True)

    base =  alt.Chart(gammaDist)
    altPlotGamma =base.mark_bar().encode(
        x="Giorni",
        y="Distribuzione dei decessi",
    ).add_selection(
        multi
    ).interactive()

    mediaPlot=base.mark_rule(color='red').encode(
        x="media",
        size=alt.value(0.5)
    ).interactive()


    st.altair_chart(altPlotGamma+mediaPlot, use_container_width=True)



    st.write("Ora possiamo riprendere i dati disponibili giornalmente su "
        "[github](https://github.com/pcm-dpc/COVID-19) "
        "pubblicati dalla protezione civile, che sono più aggiornati ma più imprecisi di quelli dell'ISS.")
    st.write("""
        Usando la distribuzione di ritardo di decesso trovata sopra, possiamo dai casi
        dedurre la curva dei decessi, fissando una letalità.

        Questo significa prendere i casi di ogni giorno, moltiplicarli per la letalità
        e aggiungere la percentuale che la distribuzione gamma ci dice avverrà tra n giorni
        nel corrispettivo giorno. Matematicamente questa operazione si chiama convoluzione e si può scrivere come
        """) 
    st.latex(r"D(i) = \sum_{k=1}^i L \cdot C(k) \cdot p(i-k)")
    st.write(r"Dove $D(i)$ sono i decessi nel giorno $i$, $C(k)$ sono i casi nel giorno $k$, "
        "$L$ è la letalità e $p(i-k)$ è la probabilità che il decesso avvenga dopo $i-k$ giorni"
        " dataci dalla distribuzione gamma.")


    source = pd.DataFrame({})

    startDay = 7


    source = source.append(
        pd.DataFrame({
        'Time':dateValues[startDay:],
        'Casi/decessi al giorno': np.array(let*casi_convoluti[startDay:len(dateValues)]),
        'Decessi':np.array(let*casi_convoluti[startDay:len(dateValues)]),
        'Classe':'Casi convoluti'
    }))
    source = source.append(
        pd.DataFrame({
        'Time':dateValues[startDay:],
        'Casi/decessi al giorno': np.array(nuovi_decessi_average[startDay:]),
        'Decessi':np.array(nuovi_decessi_average[startDay:]),
        'Classe':'Decessi'
    }))
    # source = source.append(
    #     pd.DataFrame({
    #         'Time':dateValues,
    #         'Casi/decessi al giorno': np.array(nuovi_positivi_average),
    #         'Decessi':np.array(nuovi_positivi_average*let),
    #         'Classe':'Casi'
    # }))


    altPlot= alt.Chart(source).mark_line().encode(
        alt.Y('Decessi', scale=alt.Scale(type='log',domain=[2, 5000])),
        x='Time',
        color=alt.Color('Classe', legend=alt.Legend(
                orient='none',
                legendX=20, legendY=0,
                direction='vertical',
                titleAnchor='middle',
                fillColor="gray",
                labelFontSize=14)),
        strokeDash='Classe', 
        tooltip=['Time','Classe', 'Casi/decessi al giorno']
        ).properties(
            title=f'Casi convoluti con Gamma a letalità {let} e decessi'
        ).add_selection(
            multi
        ).interactive()
    st.altair_chart(altPlot, use_container_width=True)



    source2 = pd.DataFrame({
        'Time':dateValues[startDay:],
        'CFR': np.array(nuovi_decessi_average[startDay:]/casi_convoluti[startDay:len(dateValues)])
    })

    altPlot2= alt.Chart(source2).mark_line().encode(
            alt.Y('CFR', scale=alt.Scale(domain=[0, 0.04])),
            x='Time',
            tooltip=['Time','CFR']
            ).interactive()

    st.altair_chart(altPlot2, use_container_width=True)

    #st.bar_chart(gammaDist['Distribuzione dei decessi'])

    #caption, fig, fig2 = 
#     plotCovidFigure(
#         nuovi_decessi_average, nuovi_positivi_average, nuovi_TI_average, TI, ospedalizzati, dateValues,
#                                                #endDate,
#                                                #startDate,
#                                                let,
#                                                ospCases,
#                                                ICUCases,
#                                                newICUCases,
#                                                deathsShift,
#                                                hospShift ,
#                                                ICUShift , 
#                                                newICUshift,
#                                                logScale)
# #    st.pyplot(fig)
#    st.pyplot(fig2)

    st.write("""
        Qua sopra, al contrario, calcoliamo la letalità appartente giornaliera facendo
         divisione tra decessi e casi convoluti con la gamma. 
        """)




