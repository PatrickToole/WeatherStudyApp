import requests
import os
import glob
import pandas as pd

# original website
# 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=43406&Year=2019&Month=12&Day=9&timeframe=1&submit=Download+Data'

# scrape website for weather station data

for month in range(1, 13):
    year = 2021
    month += 0
    station_id = 43406  # 43406:Bedford Basin; 43123:Bedford Range; 6302:Bedford

    climate_url = f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={year}&Month={month}&Day=9&timeframe=1&submit=Download+Data'
    month_name = ['none', '01', '02', '03', '04',
                  '05', '06', '07', '08', '09', '10', '11', '12']
    r = requests.get(climate_url)
    with open(f'Environment Canada {year}-{month_name[month]}.csv', 'wb') as f:
        f.write(r.content)

# combine all weather station data into one file
cwd = os.getcwd()
os.chdir(cwd)

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv(
    f'EnvironmentCanada{year}.csv', index=False, encoding='utf-8-sig')

os.remove(f'Environment Canada {year}-01.csv')
os.remove(f'Environment Canada {year}-02.csv')
os.remove(f'Environment Canada {year}-03.csv')
os.remove(f'Environment Canada {year}-04.csv')
os.remove(f'Environment Canada {year}-05.csv')
os.remove(f'Environment Canada {year}-06.csv')
os.remove(f'Environment Canada {year}-07.csv')
os.remove(f'Environment Canada {year}-08.csv')
os.remove(f'Environment Canada {year}-09.csv')
os.remove(f'Environment Canada {year}-10.csv')
os.remove(f'Environment Canada {year}-11.csv')
os.remove(f'Environment Canada {year}-12.csv')
