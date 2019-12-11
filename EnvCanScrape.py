import requests
import os
import glob
import pandas as pd

# original website
# 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=43406&Year=2019&Month=12&Day=9&timeframe=1&submit=Download+Data'

#scrape website for weather station data

for month in range(1, 13):
    year = 2019
    month += 0

    climate_url = f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=43406&Year={year}&Month={month}&Day=9&timeframe=1&submit=Download+Data'
    month_name = ['none','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    r = requests.get(climate_url)
    with open(f'Environment Canada {year}-{month_name[month]}.csv', 'wb') as f:
        f.write(r.content)

# combine all weather station data into one file
os.chdir('C:\\Users\\toolep\\PycharmProjects\\WeatherStudyApp')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv('EnvironmentCanada2019.csv', index=False, encoding='utf-8-sig')

os.remove('Environment Canada 2019-01.csv')
os.remove('Environment Canada 2019-02.csv')
os.remove('Environment Canada 2019-03.csv')
os.remove('Environment Canada 2019-04.csv')
os.remove('Environment Canada 2019-05.csv')
os.remove('Environment Canada 2019-06.csv')
os.remove('Environment Canada 2019-07.csv')
os.remove('Environment Canada 2019-08.csv')
os.remove('Environment Canada 2019-09.csv')
os.remove('Environment Canada 2019-10.csv')
os.remove('Environment Canada 2019-11.csv')
os.remove('Environment Canada 2019-12.csv')