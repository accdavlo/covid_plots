import tweepy
import numpy as np
import csv
import pandas as pd
import datetime
import time
from utilsTwitterCovid import *

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2


link ="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

#job=False
#while not job:
while True:
  req = Request(link)
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
  content = urlopen(req)
  dataCovid = pd.read_csv(content)
  date=dataCovid['data'].to_numpy()
  lastDateString=date[-1]
  lastDay=datetime.date(int(lastDateString[0:4]),int(lastDateString[5:7]),int(lastDateString[8:10]))
  ora = datetime.datetime.now()
  if ora.hour>=14 and ora.hour<=19:
    sys.stdout.write('\r')
    sys.stdout.write("It might be time for an update           ")
    sys.stdout.flush()
    if datetime.date.today()==lastDay:
      sys.stdout.write('\r')
      sys.stdout.write("The update arrived , time %2d:%2d:%2d (GMT) \n"%(ora.hour,ora.minute,ora.second))
      sys.stdout.write(" ")
      sys.stdout.flush()
      try:
        caption,figureName = plotCovidFigure(dataCovid)
        post1,post2=writePost(dataCovid)
      except:
        sys.stdout.write("I wasn't able to plot or post the plot")
        sys.stdout.write(" ")
        sys.stdout.flush()
      try:
        publishFigure(caption,figureName)
        publishPost(post1,post2)
      except:
        sys.stdout.write("I wasn't able to write or post the decessi post")
        sys.stdout.write(" ")
        sys.stdout.flush()
      sys.stdout.write("Done my job! \n")
      sys.stdout.write(" ")
      sys.stdout.flush()
#      job=True
      while datetime.date.today()==lastDay:
        sys.stdout.write('\r')
        sys.stdout.write("Today %s I've already done my job, it's %d (GMT)"%(datetime.date.today().isoformat(),datetime.datetime.now().hour))
        sys.stdout.flush()
        time.sleep(60*60)
    else:
      sys.stdout.write('\r')
      sys.stdout.write("Still not update, time %2d:%2d:%2d (GMT)               "%(ora.hour,ora.minute,ora.second))
      sys.stdout.flush()
      time.sleep(60)
  else:
    # the exact output you're looking for:
    sys.stdout.write('\r')
    sys.stdout.write("It's still %d (GMT), I will wait another hour                "%(datetime.datetime.now().hour))
    sys.stdout.flush()
    time.sleep(60*60)

