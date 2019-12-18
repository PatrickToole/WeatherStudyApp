import tkinter.filedialog as filedialog
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import xlsxwriter
import os

master = tk.Tk()
master.title('WeatherStudyApp Data Analysis')

expNameFontSize = 16


def input():
    input_path = tk.filedialog.askopenfilename()
    input_entry.delete(0, tk.END)  # Remove current text in entry
    input_entry.insert(0, input_path)  # Insert the 'path'


def input2():
    path = tk.filedialog.askopenfilename()
    output_entry.delete(0, tk.END)  # Remove current text in entry
    output_entry.insert(0, path)  # Insert the 'path'





top_frame = tk.Frame(master)
bottom_frame = tk.Frame(master)
line = tk.Frame(master, height=1, width=400, bg="grey80", relief='groove')

startTimeLabel = tk.Label(top_frame, text='Start Time (yyyy-mm-dd hh:mm:ms)')
startTimeEntry = tk.Entry(top_frame)
startTimeEntry.pack(side=tk.TOP)
startTimeLabel.pack(side=tk.TOP)


endTimeLabel = tk.Label(bottom_frame, text='end time (yyyy-mm-dd hh:mm:ms)')
endTimeEntry = tk.Entry(bottom_frame)
endTimeEntry.pack(side=tk.TOP)
endTimeLabel.pack(side=tk.TOP)



radLabel = tk.Label(master, text='Radius')
radLabel.pack(side=tk.LEFT)
radiusIn = tk.StringVar(master)
smallRing = 0.031
largeRing = 0.051
radiusIn.set(largeRing) # default value
w = tk.OptionMenu(master, radiusIn, smallRing, largeRing)
w.pack(side=tk.LEFT)


input_path = tk.Label(top_frame, text="WeatherStudyApp File:")
input_entry = tk.Entry(top_frame, text="", width=40)
browse1 = tk.Button(top_frame, text="Browse", command=input)

output_path = tk.Label(bottom_frame, text="Enviorment Canada File:")
output_entry = tk.Entry(bottom_frame, text="", width=40)
browse2 = tk.Button(bottom_frame, text="Browse", command=input2)



top_frame.pack(side=tk.TOP)
line.pack(pady=10)
bottom_frame.pack(side=tk.BOTTOM)

input_path.pack(pady=5)
input_entry.pack(pady=5)
browse1.pack(pady=5)

output_path.pack(pady=5)
output_entry.pack(pady=5)
browse2.pack(pady=5)






def begin():
    fileName = input_entry.get()
    fileName2 = output_entry.get()
    df = pd.read_csv(fileName, skiprows=2)
    startTime = startTimeEntry.get()
    endTime = endTimeEntry.get()
    # DF1

    Time = df.iloc[:, 1]
    Time = pd.to_datetime(Time)
    df = df[(Time >= startTime) & (Time <= endTime)]
    df.to_csv('data.csv')##############################
    time = df.iloc[:, 1]
    time = pd.to_datetime(time)

    Time_delta = time - time.min()
    Time_delta = Time_delta / np.timedelta64(1, 'h')
    Temperature = df.iloc[:, 2]
    Temperature_avg = np.nanmean(Temperature)

    if Temperature_avg > 25:
        Temperature = ((Temperature - 32) * 5 / 9)
    else:
        Temperature = Temperature

    #WATER TEMP PLOT
    x = Time_delta
    y = Temperature
    if y.max() > 16:
        y_water_max = y.max()
    else:
        y_water_max = 16

    if y.min() < 0:
        y_water_min = y.min()
    else:
        y_water_min = 0

    expName = os.path.basename(fileName)
    plt.figure()
    plt.ylim(y_water_min, y_water_max)
    plt.xlim(0, 170)
    plt.ylabel('Temperature (C)');
    plt.xlabel('Time (hours)')
    plt.plot(x, y)
    plt.suptitle(expName.rstrip('.csv'), fontsize=expNameFontSize)
    plt.title('Water Temperature')
    plt.savefig(fileName.rstrip('.csv') + 'watertempplot')

    Light = df.iloc[:, 3]
    # LIGHT PLOT
    x = Time_delta
    y = Light
    if np.max(y) > 150000:
        y_light_max = 150000
    elif np.max(y) < 80000:
        y_light_max = 80000
    else:
        y_light_max = np.max(y)
    plt.figure()
    plt.ylim(0, y_light_max)
    plt.xlim(0, 170)
    plt.ylabel('Light Intensity(Lux)');
    plt.xlabel('Time (hours)')
    plt.suptitle(expName.rstrip('.csv'), fontsize=expNameFontSize)
    plt.plot(x, y)
    plt.title('Light')
    plt.savefig(fileName.rstrip('.csv') + 'lightplot')


    radius = float(radiusIn.get())
    Temperature_avg = np.nanmean(Temperature)
    Temperature_error = np.nanstd(Temperature)
    Light_total_intensity = np.nansum(Light)
    Light_intensity_Error = np.nanstd(Light)
    Light_total_energy = (Light_total_intensity * math.pi * (radius ** 2)) / 105

    ######################################
    df = pd.read_csv('data.csv', skiprows=1)##############################
    time = df.iloc[:, 2]
    time = pd.to_datetime(time)
    temperature = df.iloc[:, 3]

    time_delta = time - time.min()
    time_delta = time_delta / np.timedelta64(1, 'h')

    plt.figure()
    x = time_delta
    y = temperature
    plt.ylabel('Temperature (C)')
    plt.xlabel('Time(hours)')
    plt.plot(x, y, color='blue', label='Raw')
    plt.suptitle(expName.rstrip('.csv'), fontsize=expNameFontSize)
    plt.title('Avg Water Temp')

    rolling_water_temp_hour = y.rolling(6, min_periods=1).mean()
    rolling_water_temp_day = y.rolling(144, min_periods=1).mean()

    y = rolling_water_temp_hour
    plt.plot(x, y, color='green', label='hour(previous 6 time points)')
    y = rolling_water_temp_day
    plt.plot(x, y, color='red', label='day(previous 144 time points)')

    plt.legend()
    # plt.show()
    plt.savefig('example rolling')
    ########################################

    ### DF2


    df = pd.read_csv(fileName2)

    Time = df.iloc[:, 4]
    Time = pd.to_datetime(Time)
    df = df[(Time >= startTime) & (Time <= endTime)]
    df.drop_duplicates(subset='Date/Time', keep='first', inplace=True)

    time = df.iloc[:, 4]
    time = pd.to_datetime(time)
    timeDelta = time - time.min()
    timeDelta = timeDelta / np.timedelta64(1, 'h')
    airTemp = df.iloc[:, 9]
    windSpeed = df.iloc[:, 17]

    #AIR TEMP PLOT

    x = timeDelta
    y = airTemp
    if y.max() < 20:
        y_air_max = 20
    else:
        y_air_max = y.max()

    if y.min() < 0:
        y_air_min = y.min()
    else:
        y_air_min = 0

    plt.figure()
    plt.ylim(y_air_min, y_air_max)
    plt.xlim(0, 170)
    plt.ylabel('Air Temperature(C)');
    plt.xlabel('Time (hours)')
    plt.plot(x, y)
    plt.suptitle(expName.rstrip('.csv'), fontsize=expNameFontSize)
    plt.title('Air Temperature')
    plt.savefig(fileName.rstrip('.csv') + 'airtempplot')

    # WIND SPEED PLOT

    x = timeDelta
    y = windSpeed

    plt.figure()
    plt.ylim(0, 60)
    plt.xlim(0, 170)
    plt.ylabel('Wind Speed(km/h)');
    plt.xlabel('Time (hours)')
    plt.plot(x, y)
    plt.suptitle(expName.rstrip('.csv'), fontsize=expNameFontSize)
    plt.title('Wind Speed')
    plt.savefig(fileName.rstrip('.csv') + 'windspeed')

    avgAirTemp = np.nanmean(airTemp)
    stdAirTemp = np.nanstd(airTemp)
    avgWindSpeed = np.nanmean(windSpeed)
    stdWindSpeed = np.nanstd(windSpeed)

    workbook = xlsxwriter.Workbook(fileName.rstrip('.csv') + 'processed.xlsx', {'nan_inf_to_errors': True})#
    worksheet = workbook.add_worksheet('Summary Data')

    worksheet.write('C1', 'Stdev')
    worksheet.write('D1', 'n value')

    worksheet.write('A2', 'Average Temperature(C)')
    worksheet.write('B2', round((float(Temperature_avg)),1))
    worksheet.write('C2', round((float(Temperature_error)),1))
    worksheet.write('D2', len(Temperature))

    worksheet.write('A3', 'Total Light Intensity (Lux)')
    worksheet.write('B3', round((float(Light_total_intensity)),1))
    worksheet.write('C3', round((float(Light_intensity_Error)),1))
    worksheet.write('D3', len(Light))

    worksheet.write('A4', 'Total Light Energy (W)')
    worksheet.write('B4', round((float(Light_total_energy)),1))
    worksheet.write('D4', len(Light))

    worksheet.write('A5', 'Average Air Temperature(C)')
    worksheet.write('B5', round((float(avgAirTemp)),1))
    worksheet.write('C5', round((float(stdAirTemp)),1))
    worksheet.write('D5', len(airTemp))

    worksheet.write('A6', 'Average Wind Speed(km/h)')
    worksheet.write('B6', round((float(avgWindSpeed)),1))
    worksheet.write('C6', round((float(stdWindSpeed)),1))
    worksheet.write('D6', len(windSpeed))

    worksheet.insert_image('E3', fileName.rstrip('.csv') + 'watertempplot.png')
    worksheet.insert_image('O3', fileName.rstrip('.csv') + 'lightplot.png')
    worksheet.insert_image('E30', fileName.rstrip('.csv') + 'airtempplot.png')
    worksheet.insert_image('O30', fileName.rstrip('.csv') + 'windspeed.png')
    ##############################################################

    worksheet_2 = workbook.add_worksheet('Rolling Avg Water Temp')

    worksheet_2.write('A1', 'Time')
    worksheet_2.write('B1', 'Raw Temp')
    worksheet_2.write('C1', 'Rolling Average Hourly')
    worksheet_2.write('D1', 'Rolling Average Daily')
    worksheet_2.insert_image('E3', 'example rolling.png')

    for item in range(len(time_delta)):
        worksheet_2.write(item + 1, 0, time_delta[item])
        worksheet_2.write(item + 1, 1, temperature[item])
        worksheet_2.write(item + 1, 2, rolling_water_temp_hour[item])
        worksheet_2.write(item + 1, 3, rolling_water_temp_day[item])

    ######################################################
    workbook.close()

    os.remove(fileName.rstrip('.csv') + 'windspeed.png')
    os.remove(fileName.rstrip('.csv') + 'airtempplot.png')
    os.remove(fileName.rstrip('.csv') + 'lightplot.png')
    os.remove(fileName.rstrip('.csv') + 'watertempplot.png')
    os.remove('data.csv')
    os.remove('example rolling.png')
begin_button = tk.Button(bottom_frame, text='Begin!', command=begin)
begin_button.pack(pady=20, fill=tk.X)
master.mainloop()
