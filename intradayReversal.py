#In this program, I'm trying to find out the instances in which a NIFTY 200 stock had made a sharp intraday reversal from day's high to close at day's low(after opening at gap up)

import pandas as pd
from nsepy import get_history
from datetime import date

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

nifty200symbolNames = ['ACC','AUBANK','AARTIIND','ADANIENT','ADANIGREEN','ADANIPORTS','ATGL','ADANITRANS','ABCAPITAL','ABFRL','AJANTPHARM','APLLTD','ALKEM','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASHOKLEY','ASIANPAINT','ASTRAL','AUROPHARMA','DMART','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BAJAJHLDNG','BALKRISIND','BANDHANBNK','BANKBARODA','BANKINDIA','BATAINDIA','BERGEPAINT','BEL','BHARATFORG','BHEL','BPCL','BHARTIARTL','BIOCON','BOSCHLTD','BRITANNIA','CADILAHC','CANBK','CASTROLIND','CHOLAFIN','CIPLA','CUB','COALINDIA','COFORGE','COLPAL','CONCOR','COROMANDEL','CROMPTON','CUMMINSIND','DLF','DABUR','DALBHARAT','DEEPAKNTR','DHANI','DIVISLAB','DIXON','LALPATHLAB','DRREDDY','EICHERMOT','EMAMILTD','ENDURANCE','ESCORTS','EXIDEIND','FEDERALBNK','FORTIS','GAIL','GMRINFRA','GLAND','GLENMARK','GODREJCP','GODREJIND','GODREJPROP','GRASIM','GUJGASLTD','GSPL','HCLTECH','HDFCAMC','HDFCBANK','HDFCLIFE','HAVELLS','HEROMOTOCO','HINDALCO','HAL','HINDCOPPER','HINDPETRO','HINDUNILVR','HINDZINC','HDFC','ICICIBANK','ICICIGI','ICICIPRULI','ISEC','IDFCFIRSTB','ITC','INDIAMART','INDIANB','INDHOTEL','IOC','IRCTC','IRFC','IGL','INDUSTOWER','INDUSINDBK','NAUKRI','INFY','INDIGO','IPCALAB','JSWENERGY','JSWSTEEL','JINDALSTEL','JUBLFOOD','KOTAKBANK','L&TFH','LTTS','LICHSGFIN','LTI','LT','LAURUSLABS','LUPIN','MRF','MGL','M&MFIN','M&M','MANAPPURAM','MARICO','MARUTI','MFSL','MINDTREE','MPHASIS','MUTHOOTFIN','NATCOPHARM','NMDC','NTPC','NATIONALUM','NAVINFLUOR','NESTLEIND','NAM-INDIA','OBEROIRLTY','ONGC','OIL','PIIND','PAGEIND','PETRONET','PFIZER','PIDILITIND','PEL','POLYCAB','PFC','POWERGRID','PRESTIGE','PGHH','PNB','RBLBANK','RECLTD','RELIANCE','SBICARD','SBILIFE','SRF','SANOFI','SHREECEM','SRTRANSFIN','SIEMENS','SBIN','SAIL','SUNPHARMA','SUNTV','SYNGENE','TVSMOTOR','TATACHEM','TATACOMM','TCS','TATACONSUM','TATAELXSI','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','RAMCOCEM','TITAN','TORNTPHARM','TORNTPOWER','TRENT','UPL','ULTRACEMCO','UNIONBANK','UBL','MCDOWELL-N','VBL','VEDL','IDEA','VOLTAS','WHIRLPOOL','WIPRO','YESBANK','ZEEL']

startYear = 2000
startMonth = 1
startDate = 1

todayDate = date.today()

endYear = todayDate.year
endMonth = todayDate.month
endDate = todayDate.day

'''
endYear = 2021
endMonth = 12
endDate = 31
'''

eventInfo = {} #{year: {symbolName: []}}; nested dictionary with value of outermost dictionary also a dictionary whose value is of list type.
path = "C:\\data\\Stock Market Data\\daily stock data\\"

nFailures = 0
for symbolName in nifty200symbolNames:
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


    savePath = path + symbolName + ".pkl"
    l_symbolData.to_pickle(savePath)

    l_symbolData = l_symbolData[~l_symbolData.index.duplicated(keep='first')]
    #print(list(l_symbolData.columns.values))

    l_symbolData = l_symbolData[['Symbol','Prev Close','Open','High','Low','Close','Last','Deliverable Volume','Volume']]
    l_symbolData['%DeliveryVolume'] = (l_symbolData['Deliverable Volume'] / l_symbolData['Volume'] ) * 100

    #l_filteredData = l_symbolData[(l_symbolData['Open'] > l_symbolData['Prev Close']) & (l_symbolData['Open'] > l_symbolData['Last'].shift(1)) & (l_symbolData['High'] > (l_symbolData['Prev Close'] * 1.06)) & (l_symbolData['Prev Close'] > (l_symbolData['Close'] * 1.1))]
    l_filteredData = l_symbolData[(l_symbolData['Open'] > l_symbolData['Prev Close']) & (l_symbolData['Open'] > l_symbolData['Last'].shift(1)) & (l_symbolData['High'] > (l_symbolData['Prev Close'] * 1.06)) & (l_symbolData['Prev Close'] > (l_symbolData['Last'] * 1.1))]

    if l_filteredData.shape[0] != 0:
        print("\nprinting data of ", symbolName)

        for index, values in l_filteredData.iterrows():
            year = str(index.year)
            l_date = index.strftime("%d/%m/%Y")

            innerDict = {}

            if year not in eventInfo:
                innerDict = {symbolName: [l_date, ]}
            else:
                innerDict = eventInfo[year]

                if symbolName not in innerDict:
                    innerDict.update({symbolName: [l_date, ]})

                else:
                    innerDict[symbolName].append(l_date)

            eventInfo[year] = innerDict

        pd.set_option('display.max_rows', l_filteredData.shape[0] + 1)
        print(l_filteredData)

for year, values in eventInfo.items():
    print("\nYear-->",year)
    for scrip,dateList in values.items():
        print("\n\tSymbol-->",scrip)
        for eventDate in dateList:
            print("\t\tDate --> ",eventDate)




# Output
Year--> 2000

	Symbol--> SRTRANSFIN
		Date -->  21/08/2000
		Date -->  26/09/2000
		Date -->  29/11/2000

	Symbol--> TATACOMM
		Date -->  21/06/2000

	Symbol--> WIPRO
		Date -->  08/05/2000


Year--> 2001

	Symbol--> BEL
		Date -->  02/03/2001

	Symbol--> HCLTECH
		Date -->  11/04/2001

	Symbol--> INFY
		Date -->  11/04/2001

	Symbol--> MPHASIS
		Date -->  02/11/2001

	Symbol--> TVSMOTOR
		Date -->  26/04/2001

	Symbol--> TATAELXSI
		Date -->  17/09/2001

	Symbol--> WIPRO
		Date -->  11/04/2001

Year--> 2002

	Symbol--> BEL
		Date -->  28/02/2002

	Symbol--> LICHSGFIN
		Date -->  28/02/2002

	Symbol--> NATCOPHARM
		Date -->  15/07/2002
		Date -->  26/07/2002

	Symbol--> SRTRANSFIN
		Date -->  16/05/2002

	Symbol--> SAIL
		Date -->  28/02/2002

Year--> 2003

	Symbol--> BAJFINANCE
		Date -->  10/07/2003

	Symbol--> SAIL
		Date -->  19/08/2003
		Date -->  20/08/2003


Year--> 2004

	Symbol--> BIOCON
		Date -->  13/04/2004

	Symbol--> CONCOR
		Date -->  14/05/2004

	Symbol--> M&M
		Date -->  17/05/2004

	Symbol--> VEDL
		Date -->  03/05/2004

Year--> 2006

	Symbol--> COROMANDEL
		Date -->  08/06/2006

	Symbol--> ESCORTS
		Date -->  22/05/2006

	Symbol--> FEDERALBNK
		Date -->  22/05/2006

	Symbol--> INDUSINDBK
		Date -->  22/05/2006

	Symbol--> SRF
		Date -->  19/05/2006
		Date -->  22/05/2006

	Symbol--> TVSMOTOR
		Date -->  22/05/2006

Year--> 2007

	Symbol--> ESCORTS
		Date -->  21/11/2007

	Symbol--> HAVELLS
		Date -->  18/10/2007

	Symbol--> UNIONBANK
		Date -->  19/10/2007


Year--> 2008

	Symbol--> AUROPHARMA
		Date -->  29/10/2008

	Symbol--> BAJFINANCE
		Date -->  21/01/2008

	Symbol--> DLF
		Date -->  05/11/2008

	Symbol--> EMAMILTD
		Date -->  11/02/2008
		Date -->  17/10/2008

	Symbol--> HINDZINC
		Date -->  07/10/2008

	Symbol--> IOC
		Date -->  21/01/2008

	Symbol--> MPHASIS
		Date -->  27/10/2008

	Symbol--> NMDC
		Date -->  13/03/2008

	Symbol--> NAVINFLUOR
		Date -->  13/03/2008

	Symbol--> TVSMOTOR
		Date -->  21/01/2008

	Symbol--> TCS
		Date -->  17/10/2008

	Symbol--> TATAMOTORS
		Date -->  27/10/2008

	Symbol--> TATASTEEL
		Date -->  05/11/2008

	Symbol--> TECHM
		Date -->  29/10/2008

	Symbol--> UBL
		Date -->  20/10/2008


Year--> 2009

	Symbol--> BATAINDIA
		Date -->  26/05/2009

	Symbol--> GSPL
		Date -->  19/05/2009

	Symbol--> MFSL
		Date -->  06/07/2009

	Symbol--> MINDTREE
		Date -->  21/07/2009

	Symbol--> SIEMENS
		Date -->  12/01/2009

Year--> 2011

	Symbol--> UNIONBANK
		Date -->  24/10/2011

Year--> 2017

	Symbol--> IDEA
		Date -->  20/03/2017

Year--> 2019

	Symbol--> YESBANK
		Date -->  01/10/2019

Year--> 2020

	Symbol--> BAJAJHLDNG
		Date -->  24/03/2020

	Symbol--> INDUSINDBK
		Date -->  17/03/2020

	Symbol--> JINDALSTEL
		Date -->  03/04/2020

	Symbol--> IDEA
		Date -->  24/02/2020
		Date -->  17/03/2020
		Date -->  18/03/2020
		Date -->  01/09/2020

	Symbol--> YESBANK
		Date -->  20/03/2020
		Date -->  24/03/2020

Year--> 2021

	Symbol--> BANKINDIA
		Date -->  19/02/2021

	Symbol--> IRCTC
		Date -->  19/10/2021
