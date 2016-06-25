__author__ = 'apple'

import requests
import json
import dateutil.parser
#import pandas as pd
from pprint import pprint
from pyhighcharts import Chart, ChartTypes
import operator
companyName='Trans'
companyName='Apple'

#companyName = 'Wells Fargo'
#companyName = 'Chase'
#companyName = "Kaiser"
from operator import itemgetter
#from pyzipcode import ZipCodeDatabase


url = "https://data.consumerfinance.gov/api/views/c8k9-ryca/rows.json?accessType=DOWNLOAD"
#jhzv-w97w
url = "https://data.consumerfinance.gov/resource/jhzv-w97w.json?company="+companyName
#url = "https://data.consumerfinance.gov/resource/s6ew-h6mp.json?company="+companyName


url = "https://data.consumerfinance.gov/resource/jhzv-w97w.json?$where=company like '%"+companyName+"%'"

#https://open.whitehouse.gov/resource/9j92-xfdk.json?$where=position_title like '%25ASSISTANT%25'

#https://open.whitehouse.gov/resource/9j92-xfdk.json?$where=position_title like '%25ASSISTANT%25'
data = requests.get(url,verify=False) #.json()
#print data
jsonData = json.loads(data.text)

cols = len(jsonData)
yearMonthMap = {}
stateCountMap = {}
zipCodeCountMap={}
allL = []
zipCodeCountMapTpl = []



def getZip(zip):
    try:
        if 'X' not in zip:
            #zcdb = ZipCodeDatabase()
            #zipc = zcdb[zip]
            #return zipc.city + ", " + zipc.state
   	    return "NA" 
    except:
        return "NA"


def dateFormatter(dateString):
    #print dateString
    yourdate = dateutil.parser.parse(dateString)
    #print str(yourdate.year) + "---" + str(yourdate.month)

    key = str(yourdate.year) + '---' + str(yourdate.month)
    if key in yearMonthMap:
        yearMonthMap[key] += 1

    else:
        yearMonthMap[key] = 1


    #return jsonData[i]['date_sent_to_company']

#print(jsonData)
for i in range(len(jsonData)):
    try:
        dateFormatter(str(jsonData[i]['date_sent_to_company']))
    except:
        continue
    if 'state' in jsonData[i]:
        key2 = str(jsonData[i]['state'])
    else:
        print jsonData[i]
        continue


    if 'zip_code' in jsonData[i]:
        key3 = getZip(str(jsonData[i]['zip_code']))
        if key3 is not 'NA':
            if key3 in zipCodeCountMap:
                zipCodeCountMap[key3] += 1
            else:
                zipCodeCountMap[key3]=1

    if key2 == 'state':
        continue
    if key2 in stateCountMap:
        stateCountMap[key2] += 1
    else:
        stateCountMap[key2] = 1
    #print jsonData[i]['date_sent_to_company']

chart = Chart()
#chart.make_3d()

#sorted_stateCountMap = sorted(stateCountMap.items(), key=operator.itemgetter(1))
#sorted_stateCountMap.reverse()


for k,v in stateCountMap.items():
    l=[]
    l.append(k)
    l.append(v)
    allL.append(l)

for k,v in zipCodeCountMap.iteritems():
    if k is not None:
        l = []
        l.append(k)
        l.append(v)
        zipCodeCountMapTpl.append(l)

chart.set_title(companyName)
chart.set_yaxis_title("Total complaints received")

chart.add_data_series(
    ChartTypes.column,
        allL,
    name="Consumer Complaints")
chart.set_options(chart={"margin": 75})

chart.set_options(xAxis={"categories":stateCountMap.keys()})
chart.show()

chart = Chart()
chart.set_title(jsonData[i]['company'])
chart.set_yaxis_title("Total complaints received")
chart.add_data_series(
    ChartTypes.column,
        zipCodeCountMapTpl,
    name="Consumer Complaints")
chart.set_options(chart={"margin": 75})
chart.set_options(xAxis={"categories":zipCodeCountMap.keys()})
chart.show()



pprint(yearMonthMap)
pprint(stateCountMap)
pprint(zipCodeCountMap)

