import pandas as pd
from nsepy import get_history
from datetime import date
from datetime import datetime, timedelta

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# disable chained assignments
pd.options.mode.chained_assignment = None

def isPinbar(startDf, endDf):
    openPrice = startDf.iloc[0]['Open']
    highPrice = max(startDf.iloc[0]['High'],endDf.iloc[0]['High'])
    lowPrice = min(startDf.iloc[0]['Low'],endDf.iloc[0]['Low'])
    closePrice = endDf.iloc[0]['Close']

    '''
    print("openPrice->",openPrice)
    print("highPrice->",highPrice)
    print("lowPrice->",lowPrice)
    print("closePrice->",closePrice)
    '''

    body = abs(closePrice-openPrice)
    upperWick = highPrice - max(closePrice,openPrice)
    lowerWick = min(openPrice,closePrice) - lowPrice

    if(lowerWick > 2 * body and upperWick < 0.9 * body):
        print(startDf.iloc[0]['Symbol']," formed a pinbar this week")
        print("body->",body)
        print("upperWick->",upperWick)
        print("lowerWick->",lowerWick,"\n")


symbolNames = ['divislab','lalpathlab','fineorg','pidilitind','icicigi','hdfcamc','britannia','grindwell','colpal','alkylamine','sbilife','tcs','nam-india','galaxysurf','kotakbank','gmmpfaudlr','marico']

endTime = date.today()
#endTime = date(2020,12,26)
startTime = endTime - timedelta(days=7)

startYear = startTime.year
startMonth = startTime.month
startDate = startTime.day

endYear = endTime.year
endMonth = endTime.month
endDate = endTime.day

for symbolName in symbolNames:
    l_symbolData = pd.DataFrame()
    while True:
        try:
            l_symbolData = get_history(symbol=symbolName,
                                       start=date(startYear, startMonth, startDate),
                                       end=date(endYear, endMonth, endDate)
                                       )
            break
        except TimeoutError:
            nFailures += 1
            print("Timeout Error",nFailures)

    l_symbolData = l_symbolData[~l_symbolData.index.duplicated(keep='first')]
    l_symbolDataTail = l_symbolData.copy()

    l_symbolDataHead = l_symbolData.head(1)
    l_symbolDataHead['%DeliveryVolume'] = (l_symbolDataHead['Deliverable Volume'] / l_symbolDataHead['Volume'] ) * 100
    l_symbolDataHead = l_symbolDataHead[['Symbol','Prev Close','Open','High','Low','Close','Last','VWAP','%DeliveryVolume']]

    l_symbolDataTail = l_symbolDataTail.tail(1)
    l_symbolDataTail['%DeliveryVolume'] = (l_symbolDataTail['Deliverable Volume'] / l_symbolDataTail['Volume'] ) * 100
    l_symbolDataTail = l_symbolDataTail[['Symbol','Prev Close','Open','High','Low','Close','Last','VWAP','%DeliveryVolume']]


    '''
    print("\nsymbol->",symbolName)
    print(l_symbolDataHead)
    print(l_symbolDataTail)
    '''
    isPinbar(l_symbolDataHead,l_symbolDataTail)
