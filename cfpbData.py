Author__ = 'apple'
import requests
import json
import dateutil.parser
from pyhighcharts import Chart, ChartTypes

class cfpbData(object):
    stateCountComplaintsChartFile = ""
    cityCountComplaintsChartFile = ""
    yearMonthMap = {}
    zipCodeCountMap={}
    stateCountMap = {}
    allL=[]
    url = ""
    jsonData = ""

    def __init__(self,companyName):
        self.companyName = companyName
        self.companyName = self.companyName.upper()
        self.url = "https://data.consumerfinance.gov/resource/jhzv-w97w.json?$where=UPPER(company) like '%"+self.companyName+"%'"
	self.stateCountMap = {}
	self.zipCodeCountMap = {}
	self.yearMonthMap = {}
	self.allL = []
	self.jsonData = ""
	self.stateCountComplaintsChartFile = ""
	self.cityCountComplaintsChartFile = ""

    def getDataSetMinDates(self):
        return min(list(self.yearMonthMap.keys()))

    def getDataSetMaxDates(self):
        return max(list(self.yearMonthMap.keys()))

    def getStateComplaintsChartFile(self):
        data = requests.get(self.url,verify=False) #.json()
        jsonData = json.loads(data.text)
        cols = len(jsonData)
        self.popStateCountMap(jsonData,cols)
	if cols < 2:
	    return ""
        for k,v in self.stateCountMap.items():
            l=[]
            l.append(k)
            l.append(v)
            self.allL.append(l)
        chart = Chart()
	Chart.cleanup_temporary_files(chart)
        #chart.set_title(self.companyName)
        try:
            chart.set_title(jsonData[0]['company'] + " (" + str.replace(self.getDataSetMinDates(),"---","-") + " To " + str.replace(self.getDataSetMaxDates(),"---","-") + ")")
        except:
            chart.set_title(self.companyName)
        chart.set_yaxis_title("Total complaints received")
        chart.add_data_series(
            ChartTypes.column,
                self.allL,
            name="Consumer Complaints")
        chart.set_options(chart={"margin": 75})
        chart.set_options(xAxis={"categories":self.stateCountMap.keys()})
        stateCountComplaintsChartFile = chart.show()
        return stateCountComplaintsChartFile
    
    def popStateCountMap(self,jsonData,cols):
	self.stateCountMap = {}
        for i in range(len(jsonData)):
            try:
                self.dateformatter(str(jsonData[i]['date_sent_to_company']))
            except:
                continue
            if 'state' in jsonData[i]:
                key2 = str(jsonData[i]['state'])
            else:
                #print jsonData[i]
                continue
            if key2 in self.stateCountMap:
                self.stateCountMap[key2] += 1
            else:
                self.stateCountMap[key2] = 1

    def dateformatter(self,dateString):
        yourdate = dateutil.parser.parse(dateString)
        key = str(yourdate.year) + '---' + str(yourdate.month)
        if key in self.yearMonthMap:
            self.yearMonthMap[key] += 1
        else:
            self.yearMonthMap[key] = 1


    def writeToMapViz(self):
         masterL = []
         for k,v in self.stateCountMap.items():
            l=[]
            l.append(k)
            l.append(v)
            masterL.append(l)
         self.writeToMapVizDataFile('static/data2.js',masterL)

    def writeToMapVizDataFile(self,fileLoc, jsonArray):
        with open(fileLoc, 'w') as outfile:
            #outfile.write("function initFunction(){ d = ")
            outfile.write("d =")
	    json.dump(jsonArray, outfile)
            outfile.write(";")
