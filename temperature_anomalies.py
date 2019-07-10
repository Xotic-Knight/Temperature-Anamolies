import pandas as pd
#convert farenheit to celcius
def fTC(f):
    c=(f-32)/1.8
    return c
#read csv
data=pd.read_csv("Book1.csv",na_values='-9999')
data=data.drop([0])
print(data)
print(23716-(len(data[data['TAVG'].isna()]))) #non-NaN Values
print(23716-len(data[data['TMIN'].isna()])) #Non NaN Values
print(data['DATE'].unique().size) #number of days
print(data[0:1]) #
print(data[-1:])
print(data['TAVG'].astype(float).mean())#Average temperature
temp=data['TMAX'].values
s=0
j=0
#TMAX temperature for Summer 69
for i in data['DATE']:
    if str(i)[2:6] == '6905' or str(i)[2:6] == '6906' or str(i)[2:6] == '6907' or str(i)[2:6] == '6908':
        s=max(s,float(temp[j]))
    j+=1
print(s)
print('----------------ONE---------------')
data['M']=(data['DATE'].astype(str)).str.slice(start=0,stop=6)
data['Month Number']=(data['DATE'].astype(str)).str.slice(start=4,stop=6)
print(data['M']) #Monthly Average Temperature
print(data['Month Number'])
data['Tempsc']=fTC(data['TAVG'].astype(float))
monthlyData=pd.DataFrame()
group_month=data.groupby('M')
for x, y in group_month:
    mean_value = y[['Tempsc']].mean()
    mean_value['M'] = x
    mean_value['Month Number']= x[4:6]
    monthlyData=monthlyData.append(mean_value,ignore_index=True)
monthlyData=monthlyData[['M','Month Number','Tempsc']]
print(monthlyData)
print("------------TWO-----------")
month_dict=pd.DataFrame({
    'Month Number':['01','02','03','04','05','06','07','08','09','10','11','12'],
    'Month':['January','February','March','April','May','June','July','August','September','October','November','December']})
period=data.ix[data['DATE'].astype(int)<19810101]#period between 1952-1980
period=period.reset_index(drop=True)
print(period)
referenceTemps=pd.DataFrame()
group_period=period.groupby('Month Number')
for x,y in group_period:
    r=y[['Tempsc']].mean()
    r['Month Number']=x
    referenceTemps=referenceTemps.append(r,ignore_index=True)
referenceTemps=referenceTemps.rename(columns={'Tempsc':'avgTempsC'})
referenceTemps=referenceTemps.merge(month_dict,on='Month Number')
print(referenceTemps)
monthlyData=monthlyData.merge(referenceTemps,how='left',on='Month Number',sort=False)
monthlyData['Diff']=monthlyData['Tempsc']-monthlyData['avgTempsC']
print(monthlyData)
print("----------THREE----------")