import pandas as pd
from nsepy import get_history
from datetime import date

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

nifty200symbolNames = ['ACC','AUBANK','AARTIIND','ADANIENT','ADANIGREEN','ADANIPORTS','ATGL','ADANITRANS','ABCAPITAL','ABFRL','AJANTPHARM','APLLTD','ALKEM','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASHOKLEY','ASIANPAINT','ASTRAL','AUROPHARMA','DMART','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BAJAJHLDNG','BALKRISIND','BANDHANBNK','BANKBARODA','BANKINDIA','BATAINDIA','BERGEPAINT','BEL','BHARATFORG','BHEL','BPCL','BHARTIARTL','BIOCON','BOSCHLTD','BRITANNIA','CADILAHC','CANBK','CASTROLIND','CHOLAFIN','CIPLA','CUB','COALINDIA','COFORGE','COLPAL','CONCOR','COROMANDEL','CROMPTON','CUMMINSIND','DLF','DABUR','DALBHARAT','DEEPAKNTR','DHANI','DIVISLAB','DIXON','LALPATHLAB','DRREDDY','EICHERMOT','EMAMILTD','ENDURANCE','ESCORTS','EXIDEIND','FEDERALBNK','FORTIS','GAIL','GMRINFRA','GLAND','GLENMARK','GODREJCP','GODREJIND','GODREJPROP','GRASIM','GUJGASLTD','GSPL','HCLTECH','HDFCAMC','HDFCBANK','HDFCLIFE','HAVELLS','HEROMOTOCO','HINDALCO','HAL','HINDCOPPER','HINDPETRO','HINDUNILVR','HINDZINC','HDFC','ICICIBANK','ICICIGI','ICICIPRULI','ISEC','IDFCFIRSTB','ITC','INDIAMART','INDIANB','INDHOTEL','IOC','IRCTC','IRFC','IGL','INDUSTOWER','INDUSINDBK','NAUKRI','INFY','INDIGO','IPCALAB','JSWENERGY','JSWSTEEL','JINDALSTEL','JUBLFOOD','KOTAKBANK','L&TFH','LTTS','LICHSGFIN','LTI','LT','LAURUSLABS','LUPIN','MRF','MGL','M&MFIN','M&M','MANAPPURAM','MARICO','MARUTI','MFSL','MINDTREE','MPHASIS','MUTHOOTFIN','NATCOPHARM','NMDC','NTPC','NATIONALUM','NAVINFLUOR','NESTLEIND','NAM-INDIA','OBEROIRLTY','ONGC','OIL','PIIND','PAGEIND','PETRONET','PFIZER','PIDILITIND','PEL','POLYCAB','PFC','POWERGRID','PRESTIGE','PGHH','PNB','RBLBANK','RECLTD','RELIANCE','SBICARD','SBILIFE','SRF','SANOFI','SHREECEM','SRTRANSFIN','SIEMENS','SBIN','SAIL','SUNPHARMA','SUNTV','SYNGENE','TVSMOTOR','TATACHEM','TATACOMM','TCS','TATACONSUM','TATAELXSI','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','RAMCOCEM','TITAN','TORNTPHARM','TORNTPOWER','TRENT','UPL','ULTRACEMCO','UNIONBANK','UBL','MCDOWELL-N','VBL','VEDL','IDEA','VOLTAS','WHIRLPOOL','WIPRO','YESBANK','ZEEL']

todayDate = date.today()

startYear = todayDate.year
startMonth = todayDate.month
startDate = todayDate.day - 1

endYear = todayDate.year
endMonth = todayDate.month
endDate = todayDate.day - 1

def lastAboveVwap(fa_dataframe):
    l_filteredData = fa_dataframe[ (fa_dataframe['Last'] < fa_dataframe['Open']) & (fa_dataframe['Last'] > fa_dataframe['VWAP']) ]
    return l_filteredData

def lastBelowVwap(fa_dataframe):
    l_filteredData = fa_dataframe[(fa_dataframe['Last'] > fa_dataframe['Open']) & (fa_dataframe['Last'] < fa_dataframe['VWAP'])]
    return l_filteredData



nFailures = 0

filterResult_belowVwap = []
filterResult_aboveVwap = []

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

    l_symbolData = l_symbolData[~l_symbolData.index.duplicated(keep='first')]
    #print(list(l_symbolData.columns.values))


    l_symbolData['%DeliveryVolume'] = (l_symbolData['Deliverable Volume'] / l_symbolData['Volume'] ) * 100
    l_symbolData = l_symbolData[['Symbol','Prev Close','Open','High','Low','Close','Last','VWAP','%DeliveryVolume']]

    l_filteredData_belowVwap = lastBelowVwap(l_symbolData)

    if l_filteredData_belowVwap.shape[0] != 0:
        print("\n",symbolName)
        filterResult_belowVwap.append(symbolName)
        print(l_filteredData_belowVwap)

    l_filteredData_aboveVwap = lastAboveVwap(l_symbolData)
    if l_filteredData_aboveVwap.shape[0] != 0:
        print("\n",symbolName)
        filterResult_aboveVwap.append(symbolName)
        print(l_filteredData_aboveVwap)


if(len(filterResult_aboveVwap) == 0):
    print("\n\nNo stock found satifsfying 'LTP < Open & LTP > VWAP' in Nifty 200")

else:
    print("\n\n***Given below are stocks satifsfying 'LTP < Open & LTP > VWAP' in Nifty 200***")
    print("\n",filterResult_aboveVwap)

if (len(filterResult_belowVwap) == 0):
    print("\n\nNo stock found satifsfying 'LTP > Open & LTP < VWAP' in Nifty 200")

else:
    print("\n\n***Given below are stocks satifsfying 'LTP > Open & LTP < VWAP' in Nifty 200***")
    print("\n", filterResult_belowVwap)
