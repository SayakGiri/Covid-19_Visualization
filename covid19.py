import pandas as pd
import matplotlib.pyplot as plt
confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('time_series_covid19_recovered_global.csv')

#We are not interested in the coordinates and the prvince/state. We want country-wise data
confirmed = confirmed.drop(['Province/State','Lat','Long'],axis = 1)
deaths = deaths.drop(['Province/State','Lat','Long'],axis = 1)
recovered = recovered.drop(['Province/State','Lat','Long'],axis = 1)

# We want country-wise aggregate data. So we group the data country-wise and aggregate the data
confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')

#Transposing the rows and columns of the datasets
confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T
 
#To find the number of new cases everyday
new_cases = confirmed.copy()

for day in range(1,len(confirmed)):
     new_cases.iloc[day] = confirmed.iloc[day]-confirmed.iloc[day-1]
 print(new_cases.tail(10))
 
#To find the growth rate
 growth_rate = confirmed.copy()
 
 for day in range(1,len(confirmed)):
     growth_rate.iloc[day] = (new_cases.iloc[day]/confirmed.iloc[day-1])*100
 
print(growth_rate.tail(10))

#To find the number of active cases
active_cases = confirmed.copy()

for day in range(0,len(confirmed)):
     active_cases.iloc[day] = confirmed.iloc[day]-deaths.iloc[day]-recovered.iloc[day]
print(active_cases.tail(10))

#To find the actual/overall growth rate consiering only the active cases
overall_growth_rate = confirmed.copy()

for day in range(1,len(confirmed)):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day]-active_cases.iloc[day-1])/active_cases.iloc[day-1])*100
print(overall_growth_rate.tail(10))
print(overall_growth_rate['China'].tail(10))
print(overall_growth_rate['India'].tail(10))


#To find the death rate
death_rate = confirmed.copy()

for day in range(0,len(confirmed)):
    death_rate.iloc[day] = (deaths.iloc[day]/confirmed.iloc[day])*100
print(death_rate.tail(10))


#To find hospitalization rate
hospitalization_rate_estimate = 0.05

hospitalization_needed = confirmed.copy()
for day in range(0,len(confirmed)):
    hospitalization_needed.iloc[day] = active_cases.iloc[day]*hospitalization_rate_estimate


#VISUALIZATION
    
countries = ['India','Italy','US','China','Germany']

ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x',colors='white')
ax.tick_params(axis='y',colors='white')
ax.set_title('Covid-19 - Total Confirmed Cases By Country',color='white')


for country in countries:
    confirmed[country].plot(label=country)
plt.legend(loc='upper left')
plt.show()
    

#Growth Rate 

countries = ['India','Italy','US','China']
for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x',colors='white')
    ax.tick_params(axis='y',colors='white')
    ax.set_title(f'Covid-19 - Growth Rate :{country}',color='white')
    growth_rate[country].plot.bar()
    plt.show()
    
   
#Deaths

countries = ['India','Italy','US','China','Germany']

ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x',colors='white')
ax.tick_params(axis='y',colors='white')
ax.set_title('Covid-19 - Total Deaths By Country',color='white')


for country in countries:
    deaths[country].plot(label=country)
plt.legend(loc='upper left')
plt.show()
   
#Death Rate 

countries = ['India','Italy','US','China']
for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x',colors='white')
    ax.tick_params(axis='y',colors='white')
    ax.set_title(f'Covid-19 - Death Rate :{country}',color='white')
    death_rate[country].plot.bar()
    plt.show()
    
    
#Simulation if the simulated growth rate is given
simulated_growth_rate = 0.06   
dates = pd.date_range(start='4/25/20',periods=40,freq='D')
dates = pd.Series(dates)
dates = dates.dt.strftime('%m/%d/%y')

simulated = confirmed.copy()
simulated = simulated.append(pd.DataFrame(index=dates))

for day in range(len(confirmed),len(confirmed)+40):
    simulated.iloc[day] = simulated.iloc[day-1]*(1+simulated_growth_rate)
    
ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x',colors='white')
ax.tick_params(axis='y',colors='white')
ax.set_title('Future Simulation for India',color='white')
simulated['India'].plot()
plt.show()


estimated_death_rate = 0.03

#infected *death rate = deaths                (ideally)
#infected = deaths/ death rate

print(deaths['India'].tail()[4]/estimated_death_rate) #estimated total number of people infected in India
