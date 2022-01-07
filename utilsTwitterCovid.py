import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates

def plotCovidFigure(nuovi_decessi_average, nuovi_positivi_average, nuovi_TI_average, TI, ospedalizzati,
                    dateValues,
                    endDate,
                    startDate=datetime.date(2020,8,15),
                    let=0.02,
                    ospCases=0.013/0.02,
                    ICUCases=0.115/0.02,
                    newICUCases=1.7/0.02,
                    deathsShift=13,
                    hospShift=10,
                    ICUShift=12,
                    newICUshift=5,
                    logScale=True):
    print("I'm plotting")

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=600)
    
    xticksMy = []    
    for j in range(2020, 2024):
        for k in range(1, 13):
            xticksMy.append(datetime.date(j, k, 1))

    formatter = mdates.DateFormatter("%m/%y")
    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_xticks(xticksMy)
    plt.xlim([startDate, endDate])

    minMax = 50000
    if logScale:
        plt.semilogy([d - datetime.timedelta(days=hospShift) for d in dateValues],
                     ospedalizzati / ospCases, "-.", linewidth=2,
                     label=f'Ospedalizzati diviso %1.3f %d gg dopo' % (ospCases, hospShift))
        minMax = max(minMax, np.max(ospedalizzati / ospCases) * 1.5)
        plt.semilogy([d - datetime.timedelta(days=ICUShift) for d in dateValues],
                     TI / ICUCases, ":", linewidth=2,
                     label=f'Terapia Intensiva diviso %1.3f %d gg dopo' % (ICUCases, ICUShift))
        minMax = max(minMax, np.max(TI / ICUCases) * 1.5)
        plt.semilogy([d - datetime.timedelta(days=newICUshift) for d in dateValues],
                     nuovi_TI_average / newICUCases, "--", linewidth=2,
                     label=f'Nuovi ingressi in TI diviso %1.3f %d gg dopo' % (newICUCases, newICUshift))
        minMax = max(minMax, np.max(nuovi_TI_average / newICUCases) * 1.5)
        plt.semilogy(dateValues,
                     nuovi_positivi_average, "-", linewidth=2,
                     label=f'Nuovi casi')
        minMax = max(minMax, np.max(nuovi_positivi_average) * 1.5)
        plt.semilogy([d - datetime.timedelta(days=deathsShift) for d in dateValues],
                     nuovi_decessi_average/let, linewidth=2,
                     label=f"Nuovi Decessi diviso %1.3f %d gg dopo" % (let,deathsShift))
        minMax = max(minMax, np.max(nuovi_decessi_average/let) * 1.5)
        plt.legend(loc="best", bbox_to_anchor=(0.0, 0., 0.5, 0.5), framealpha=0.95)
    else:
        plt.plot([d - datetime.timedelta(days=hospShift) for d in dateValues],
                     ospedalizzati / ospCases, "-.", linewidth=2,
                     label=f'Ospedalizzati diviso %1.3f %d gg dopo' % (ospCases, hospShift))
        minMax = max(minMax, np.max(ospedalizzati / ospCases) * 1.5)
        plt.plot([d - datetime.timedelta(days=ICUShift) for d in dateValues],
                     TI / ICUCases, ":", linewidth=2,
                     label=f'Terapia Intensiva diviso %1.3f %d gg dopo' % (ICUCases, ICUShift))
        minMax = max(minMax, np.max(TI / ICUCases) * 1.5)
        plt.plot([d - datetime.timedelta(days=newICUshift) for d in dateValues],
                     nuovi_TI_average / newICUCases, "--", linewidth=2,
                     label=f'Nuovi ingressi in TI diviso %1.3f %d gg dopo' % (newICUCases, newICUshift))
        minMax = max(minMax, np.max(nuovi_TI_average / newICUCases) * 1.5)
        plt.plot(dateValues,
                     nuovi_positivi_average, "-", linewidth=2,
                     label=f'Nuovi casi')
        minMax = max(minMax, np.max(nuovi_positivi_average) * 1.5)
        plt.plot([d - datetime.timedelta(days=deathsShift) for d in dateValues],
                     nuovi_decessi_average/let, linewidth=2,
                     label=f"Nuovi Decessi diviso %1.3f %d gg dopo" % (let,deathsShift))
        minMax = max(minMax, np.max(nuovi_decessi_average/let) * 1.5)
        plt.legend(loc="best", framealpha=0.95)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    #plt.text(dateValues[-1] - datetime.timedelta(days=5), nuovi_positivi_average[-1],
    #         f"Nuovi casi {int(nuovi_positivi_average[-1]):,}", ha='right', bbox=props)
    # plt.text(dateValues[-1] - datetime.timedelta(days=newICUshift + 10), nuovi_TI_average[-1] / newICUCases * 1.1,
    #          f"Nuove TI {int(nuovi_TI_average[-1]):,}", ha='right', bbox=props)
    # plt.text(dateValues[-1] - datetime.timedelta(days=deathsShift + 10), nuovi_decessi_average[-1] /let * 0.9,
    #          f"Nuovi decessi {int(nuovi_decessi_average[-1]):,}", ha='right', bbox=props)

    plt.axvline(datetime.date(2020, 12, 27), linewidth=1, color="k", linestyle="--", label="Inizio Vaccinazioni")
    # plt.axvline(datetime.date(2021,4,18),linewidth=1,color="k",linestyle="-.",label="Vaccinati l'80% di over80 con 1+ dose")
    # plt.axvline(datetime.date(2021,5,12),linewidth=1,color="k",linestyle="--",label="Vaccinati l'80% di over70 con 1+ dose")
    # plt.axvline(datetime.date(2021,6,3),linewidth=1,color="k",linestyle="-.",label="Vaccinati l'80% di over60 con 1+ dose")
    plt.axvline(datetime.date(2021, 6, 19), linewidth=1, color="k", linestyle="-.",
                label="Vaccinati l'80% di over50 con 1+ dose")



    yticksMy = []
    for k in [100, 1000, 10000, 100000]:
        for j in range(1,10):
            yticksMy.append(k*j)

    ax1.set_yticks(yticksMy)
    ax1.set_yticklabels([str(dig) for dig in yticksMy])

    plt.ylim([100, minMax])
    plt.grid(True)
    plt.title("Covid-19 Italia (scala logaritmica)")
    #plt.text(datetime.date(2020, 10, 1), 3.3, "Grafico di Davide Torlo - Fonte dati: Protezione Civile",
    #         horizontalalignment='left', verticalalignment='center',
    #         color=[0.3, 0.3, 0.3])


    #plt.tight_layout()
    #filename = "ospedalizzati3.png"
    #plt.savefig(filename)
    mesiItaliani = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
                    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    todayDate = datetime.date.today()
    caption = f"Aggiornamento %d %s: dati in media mobile 7gg." % (todayDate.day, mesiItaliani[todayDate.month - 1])

    fig2, ax2 = plt.subplots(figsize=(10,6), dpi=600)
    plt.plot(dateValues[deathsShift+6:],
                     np.convolve(nuovi_decessi_average[deathsShift:]/nuovi_positivi_average[:-deathsShift], 1 / 7 * np.ones(7), 'valid'), linewidth=2,
                     label="Letalità apparente")
    plt.plot(dateValues[deathsShift+6:],
                     np.convolve(nuovi_TI_average[deathsShift:]/nuovi_positivi_average[:-deathsShift], 1 / 7 * np.ones(7), 'valid'), linewidth=2,
                     label="TI/casi apparente")
    plt.plot(dateValues[deathsShift+6:],let*np.ones(len(dateValues[deathsShift+6:])),":")
    plt.plot(dateValues[deathsShift+6:],newICUCases*np.ones(len(dateValues[deathsShift+6:])),":")
    plt.ylim([0,0.03])
    plt.legend(loc="best")
    ax2.xaxis.set_major_formatter(formatter)
    ax2.set_xticks(xticksMy)
    plt.xlim([startDate, endDate])
    plt.grid(True)
    plt.title("Frazioni")
    

    return caption, fig, fig2


def writePost(dataCovid):
    print("I'm writing the post")
    nuovi_positivi = dataCovid['nuovi_positivi'].to_numpy()
    maxLen = len(nuovi_positivi)

    maxDay = maxLen;
    decessiTotali = dataCovid['deceduti'].to_numpy()
    nuovi_decessi = np.zeros(maxDay)
    nuovi_decessi[1:] = decessiTotali[1:] - decessiTotali[:-1]
    dates = dataCovid['data'].to_numpy()
    dateValues = [datetime.datetime.strptime(dates[d][:10], "%Y-%m-%d").date() for d in range(1, maxLen)]

    weekNumber = int(np.ceil(maxDay / 7))
    weekCumulativePositive = np.zeros((weekNumber, 7));
    weekCumulativeDeaths = np.zeros((weekNumber, 7));
    percentageEachWeekDeaths = np.zeros(weekNumber);
    percentageEachWeekPositive = np.zeros(weekNumber);

    for w in range(1, weekNumber + 1):
        day = (w - 1) * 7 + 1;
        weekCumulativePositive[w - 1, 1 - 1] = nuovi_positivi[day - 1]
        weekCumulativeDeaths[w - 1, 1 - 1] = nuovi_decessi[day - 1];
        for dd in range(2, 8):
            day = day + 1;
            if day <= maxDay:
                weekCumulativePositive[w - 1, dd - 1] = weekCumulativePositive[w - 1, dd - 2] + nuovi_positivi[day - 1];
                weekCumulativeDeaths[w - 1, dd - 1] = weekCumulativeDeaths[w - 1, dd - 2] + nuovi_decessi[day - 1];
        if w > 1:
            percentageEachWeekDeaths[w - 1] = (weekCumulativeDeaths[w - 1, 7 - 1] - weekCumulativeDeaths[
                w - 2, 7 - 1]) / weekCumulativeDeaths[w - 2, 7 - 1];
            percentageEachWeekPositive[w - 1] = (weekCumulativePositive[w - 1, 7 - 1] - weekCumulativePositive[
                w - 2, 7 - 1]) / weekCumulativePositive[w - 2, 7 - 1];

    dayOfTheWeek = np.mod(maxDay - 1, 7) + 1;
    weekDays = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"];

    decessiString = ''

    if dayOfTheWeek == 1:
        decessiString += "Decessi del lunedì\n\n"
    else:
        decessiString += "Decessi tra lunedì e %s\n\n" % (weekDays[dayOfTheWeek - 1])

    numStr = f'{int(weekCumulativeDeaths[-1, dayOfTheWeek - 1]):,}'
    decessiString += "- questa settimana: %s\n" % (numStr)
    numStr = f'{int(weekCumulativeDeaths[-2, dayOfTheWeek - 1]):,}'
    decessiString += "- scorsa settimana: %s\n" % (numStr)
    numStr = f'{int(weekCumulativeDeaths[-3, dayOfTheWeek - 1]):,}'
    decessiString += "- due settimane fa: %s\n" % (numStr)
    numStr = f'{int(weekCumulativeDeaths[-4, dayOfTheWeek - 1]):,}'
    decessiString += "- tre settimane fa: %s\n" % (numStr)
    numStr = f'{int(weekCumulativeDeaths[-5, dayOfTheWeek - 1]):,}'
    decessiString += "- quattro settimane fa: %s\n" % (numStr)
    numStr = f'{int(weekCumulativeDeaths[-6, dayOfTheWeek - 1]):,}'
    decessiString += "- cinque settimane fa: %s\n\n" % (numStr)

    meanLast4Weeks = np.mean(weekCumulativeDeaths[-5:-1, dayOfTheWeek - 1]);
    var = (weekCumulativeDeaths[-1, dayOfTheWeek - 1] - meanLast4Weeks) / meanLast4Weeks;

    decessiString += "Variazione rispetto alla media delle ultime 4 settimane\n"
    decessiString += "- decessi: %+g %s" % (round(var * 100), "%")

    if dayOfTheWeek == 7:
        incrementiStr = ''
        incrementiStr += "Tassi di crescita dei decessi settimanali\n\n";
        incrementiStr += "- questa settimana: %+g %s\n" % (round(percentageEachWeekDeaths[w - 1] * 100), "%");
        incrementiStr += "- scorsa settimana: %+g %s\n" % (round(percentageEachWeekDeaths[w - 2] * 100), "%");
        incrementiStr += "- due settimane fa: %+g %s\n" % (round(percentageEachWeekDeaths[w - 3] * 100), "%");
        incrementiStr += "- tre settimane fa: %+g %s\n" % (round(percentageEachWeekDeaths[w - 4] * 100), "%");
        incrementiStr += "- quattro settimane fa: %+g %s\n" % (round(percentageEachWeekDeaths[w - 5] * 100), "%");
        incrementiStr += "- cinque settimane fa: %+g %s\n" % (round(percentageEachWeekDeaths[w - 6] * 100), "%");
    else:
        incrementiStr = None
    return decessiString, incrementiStr
