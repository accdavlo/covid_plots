import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
import altair as alt
import pandas as pd
import streamlit as st


def plotCovidFigure(nuovi_decessi_average, nuovi_positivi_average, nuovi_TI_average, TI, ospedalizzati,
                    dateValues,
                    # endDate,
                    # startDate=datetime.date(2020,8,15),
                    let=0.02,
                    ospCases=0.013 / 0.02,
                    ICUCases=0.115 / 0.02,
                    newICUCases=1.7 / 0.02,
                    deathsShift=13,
                    hospShift=10,
                    ICUShift=12,
                    newICUshift=5,
                    logScale=True):
    print("I'm plotting")

    source = pd.DataFrame({})

    source = source.append(
        pd.DataFrame({
            'Time': np.array([d - datetime.timedelta(days=hospShift) for d in dateValues]),
            'Popolazione': ospedalizzati,
            'Casi': ospedalizzati / ospCases,
            'Classe': 'Ospedalizzati'
        }))

    source = source.append(
        pd.DataFrame({
            'Time': np.array([d - datetime.timedelta(days=ICUShift) for d in dateValues]),
            'Popolazione': TI,
            'Casi': TI / ICUCases,
            'Classe': 'Terapia Intensiva'
        }))

    source = source.append(
        pd.DataFrame({
            'Time': np.array([d - datetime.timedelta(days=newICUshift) for d in dateValues]),
            'Popolazione': np.ceil(nuovi_TI_average),
            'Casi': nuovi_TI_average / newICUCases,
            'Classe': 'Ingressi in Terapia Intensiva'
        }))

    source = source.append(
        pd.DataFrame({
            'Time': dateValues,
            'Popolazione': np.ceil(nuovi_positivi_average),
            'Casi': nuovi_positivi_average,
            'Classe': 'Nuovi Casi'
        }))

    source = source.append(
        pd.DataFrame({
            'Time': np.array([d - datetime.timedelta(days=deathsShift) for d in dateValues]),
            'Popolazione': np.ceil(nuovi_decessi_average),
            'Casi': nuovi_decessi_average / let,
            'Classe': 'Nuovi Decessi'
        }))

    source2 = pd.DataFrame({})
    source2 = source2.append(
        pd.DataFrame({
            'Time': np.array(dateValues[deathsShift + 6:]),
            'Frazione': np.convolve(nuovi_TI_average[deathsShift:] / nuovi_positivi_average[:-deathsShift],
                                    1 / 7 * np.ones(7), 'valid'),
            'Classe': 'Tasso di Terapia Intensiva apparente'
        }))

    source2 = source2.append(
        pd.DataFrame({
            'Time': np.array(dateValues[deathsShift + 6:]),
            'Frazione': np.convolve(nuovi_decessi_average[deathsShift:] / nuovi_positivi_average[:-deathsShift],
                                    1 / 7 * np.ones(7), 'valid'),
            'Classe': 'Letalità apparente'
        }))

    source2 = source2.append(
        pd.DataFrame({
            'Time': np.array(dateValues[deathsShift + 6:]),
            'Frazione': let,
            'Classe': 'Letalità %1.2f%%' % (100 * let)
        }))
    source2 = source2.append(
        pd.DataFrame({
            'Time': np.array(dateValues[deathsShift + 6:]),
            'Frazione': newICUCases,
            'Classe': 'Tasso di TI %1.2f%%' % (100 * newICUCases)
        }))

    if logScale:
        altPlot = alt.Chart(source).transform_filter(
            alt.datum.Casi > 0
        ).mark_line().encode(
            alt.Y('Casi', scale=alt.Scale(type='log', domain=[100, 200000])),
            x='Time',
            color=alt.Color('Classe', legend=alt.Legend(
                orient='none',
                legendX=20, legendY=0,
                direction='vertical',
                titleAnchor='middle',
                fillColor="gray",
                labelFontSize=14)),
            strokeDash='Classe',
            tooltip=['Time', 'Classe', 'Popolazione']
        ).interactive()
    else:
        altPlot = alt.Chart(source).transform_filter(
            alt.datum.Casi > 0
        ).mark_line().encode(
            alt.Y('Casi'),
            x='Time',
            color=alt.Color('Classe', legend=alt.Legend(
                orient='none',
                legendX=20, legendY=0,
                direction='vertical',
                titleAnchor='middle',
                fillColor="gray",
                labelFontSize=14)),
            strokeDash='Classe',
            tooltip=['Time', 'Classe', 'Popolazione']
        ).interactive()

    st.altair_chart(altPlot, use_container_width=True)

    altPlot2 = alt.Chart(source2).mark_line().encode(
        alt.Y('Frazione', scale=alt.Scale(domain=[0, 0.05])),
        x='Time',
        color=alt.Color('Classe', legend=alt.Legend(
            orient='none',
            legendX=20, legendY=0,
            direction='vertical',
            titleAnchor='middle',
            fillColor="gray",
            labelFontSize=14)),
        strokeDash='Classe',
        tooltip=['Time', 'Classe', 'Frazione']
    ).interactive()

    st.altair_chart(altPlot2, use_container_width=True)

    return  # caption, fig, fig2


def plotCovidData(country='Italy', endDate=datetime.datetime.today(), startDate=datetime.date(2020, 8, 15), fatality=2,
                  deathDelay=12, IcuOnHospRatio=10, plotScale="linear"):
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

    source = pd.DataFrame({})

    source = source.append(
        pd.DataFrame({
            'Time': np.array(dateValuesCases),
            'Popolazione': nuoviCasAveraged,
            'Casi': nuoviCasAveraged,
            'Classe': 'Casi'
        }))

    source = source.append(
        pd.DataFrame({
            'Time': np.array(dateValuesCases),
            'Popolazione': dateValuesDeaths,
            'Casi': dateValuesDeaths / fatality,
            'Classe': 'Decessi'
        }))

    if plotScale == "logarithmic":
        altPlot = alt.Chart(source).transform_filter(
            alt.datum.Casi > 0
        ).mark_line().encode(
            alt.Y('Casi', scale=alt.Scale(type='log', domain=[100, 200000])),
            x='Time',
            color=alt.Color('Classe', legend=alt.Legend(
                orient='none',
                legendX=20, legendY=0,
                direction='vertical',
                titleAnchor='middle',
                fillColor="gray",
                labelFontSize=14)),
            strokeDash='Classe',
            tooltip=['Time', 'Classe', 'Popolazione']
        ).interactive()
    else:
        altPlot = alt.Chart(source).transform_filter(
            alt.datum.Casi > 0
        ).mark_line().encode(
            alt.Y('Casi'),
            x='Time',
            color=alt.Color('Classe', legend=alt.Legend(
                orient='none',
                legendX=20, legendY=0,
                direction='vertical',
                titleAnchor='middle',
                fillColor="gray",
                labelFontSize=14)),
            strokeDash='Classe',
            tooltip=['Time', 'Classe', 'Popolazione']
        ).interactive()
    print("ciao")
    print(source)
    print(altPlot)
    st.altair_chart(altPlot, use_container_width=True)

    fig, ax1 = plt.subplots(figsize=(6, 6))

    maxPlots = max(max(nuoviCasAveraged), max(nuoviDecAveraged / fatality * 100))

    color = 'tab:blue'

    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('New Cases per 100 000 population (7 days average)', color=color)
    if plotScale == "linear":
        ax1.plot(dateValuesCases, nuoviCasAveraged, label="Cases", color=color)
    elif plotScale == "logarithmic":
        ax1.semilogy(dateValuesCases, nuoviCasAveraged, label="Cases", color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    xticks = [datetime.date(2020, d, 1) for d in range(1, 13)]
    for d in range(1, 13):
        xticks.append(datetime.date(2021, d, 1))
    ax1.set_xticks(xticks)
    ax1.set_ylim([10 ** -3, maxPlots])
    ax1.set_xlim([datetime.date(2020, initMonth, 1), datetime.datetime.today()])
    ax1.grid(True)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('New Deaths per 100 000 population (7 days average)',
                   color=color)  # we already handled the x-label with ax1
    if plotScale == "linear":
        ax2.plot(dateValuesDeaths, nuoviDecAveraged, color=color)
    elif plotScale == "logarithmic":
        ax2.semilogy(dateValuesDeaths, nuoviDecAveraged, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xticks(xticks)
    ax2.set_ylim([10 ** -3 * fatality / 100, maxPlots * fatality / 100])
    ax2.set_xlim([datetime.date(2020, initMonth, 1), datetime.datetime.today()])

    plt.title(country)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    IcuAveraged = countryCovidData['icu_patients'].to_numpy() / pop100;
    HospAveraged = countryCovidData['hosp_patients'].to_numpy() / pop100;

    idxsNan = np.isnan(IcuAveraged)
    IcuAveraged[idxsNan] = 0
    idxsNan = np.isnan(HospAveraged)
    HospAveraged[idxsNan] = 0

    dates = countryCovidData['date'].to_numpy()
    ll = len(IcuAveraged)
    lenDates = len(dates)
    dateValuesIcu = [datetime.datetime.strptime(dates[d], "%Y-%m-%d").date() for d in range(lenDates - ll, lenDates)]
    formatter = mdates.DateFormatter("%d-%m-%Y")

    fig, ax1 = plt.subplots(figsize=(6, 6))

    maxPlots = max(max(HospAveraged), max(IcuAveraged / IcuOnHospRatio * 100))

    color = 'tab:blue'

    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Hospitalizations per 100 000 population', color=color)
    ax1.plot(dateValuesIcu, HospAveraged, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(xticks)
    ax1.set_ylim([10 ** -3, maxPlots])
    ax1.set_xlim([datetime.date(2020, initMonth, 1), datetime.datetime.today()])
    ax1.grid(True)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Total Covid Intensive Care Units per 100 000 population',
                   color=color)  # we already handled the x-label with ax1
    ax2.plot(dateValuesIcu, IcuAveraged, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xticks(xticks)
    ax2.set_ylim([0, maxPlots * IcuOnHospRatio / 100])
    ax2.set_xlim([datetime.date(2020, initMonth, 1), datetime.datetime.today()])

    plt.title(country)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
