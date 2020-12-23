import sys
import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import ( 
    DateFormatter, AutoDateLocator, AutoDateFormatter, datestr2num 
)

source = [
    'bbcbreaking', 
    'bbcworld', 
    'cnn', 
    'cnnbrk',
    'foxnews',
    'reuters',
    'theeconomist',
    'time',
    'wsj'
]

attribute = [
    'Reply no.', 
    'Retweets', 
    'Likes'
]

# take date in YYYY-MM-DD format and time in hh:mm:ss and convert into timestamp of int-minutes since 0001-01-01
def compress_datetime(date, time):
    date_num = datestr2num(date)
    timearr = time.split(":")
    time_num = (int(timearr[0])*60)+int(timearr[1])
    stamp = int((date_num*1440)+time_num)
    return stamp

# stamps for year-01-01 00:00 in the range start_year to end_year (inclusive)
def stamps_for_years_between(start_year, end_year):
    stamp = []
    for i in range(int(end_year) - int(start_year) + 1):
        raw_year = int(start_year) + i
        year = f"{raw_year:04d}"
        datetime = compress_datetime('%s-01-01' % year, '00:00')
        stamp = np.append(stamp, datetime)
    return stamp

# check that the source and attribute are correct, assigns default if not specified
def file_path_check(source_name, attribute_name):
    default_source_name = 'cnnbrk'
    default_attribute_name = 'Likes'
    
    if source_name == '':
        print('Using default source: %s' % default_source_name)
        source_name_out = default_source_name
    elif (len(list(filter (lambda x : x == source_name, source))) > 0):
        print('Selected source: %s' % source_name)
        source_name_out = source_name
    else:
        sys.exit('Unsupported source name') 
        
    if attribute_name == '':
        print('Using default attribute: %s' % default_attribute_name)
        attribute_name_out = default_attribute_name
    elif (len(list(filter (lambda x : x == attribute_name, attribute))) > 0):
        print('Selected attribute: %s' % default_source_name)
        attribute_name_out = attribute_name
    else:
        sys.exit('Unsupported attribute name')
        
    return source_name_out, attribute_name_out

# read data file from specified excel file
# !!! excel files must be in a Data folder in the same Directory as the python file
def read_file(file_name):
    path = os.getcwd()
    read_file_path = 'Data/%s_data.xlsx' % file_name
    print('Accessing data in %s' % read_file_path)
    data = pd.read_excel(r'%s/%s' % (path, read_file_path))
    print('Data from %s loaded' % read_file_path)
    return data

# read specified column from excel data and convert to array format
def read_column(data, column_name):
    column = pd.DataFrame(data, columns= ['%s' % column_name])
    array = column.to_numpy()
    column_array = array.reshape(array.shape[1],array.shape[0])[0]
    return column_array

# simple plot of two specified columns from a given excel data
def plot_columns(data, column1_name, column2_name):
    data_column1 = read_column(data, column1_name)
    data_column2 = read_column(data, column2_name)
    plt.plot(data_column1, data_column2, marker = '.', ls = '', c = 'grey')
    plt.xlabel(column1_name)
    plt.ylabel(column2_name)

# specifies one of the ploted columns to be 'timestamp' and sets scale to 'log'
def time_plot_column(data, column_name):
    plot_columns(data, 'Timestamp', column_name)
    plt.yscale('log')

# horizontal lines plotted over the attribute data    
def plot_lines(stamps, values, colour_name='k', line_label='l'):
    for i in range(len(stamps) - 1):
        if i == 0: 
            set_label = line_label
        else:
            set_label = ''
        plt.hlines(values[i], stamps[i], stamps[i+1], 
                   colors = colour_name, label=set_label, zorder = 10)

# returns yearly average (default) or standard deviation for specified attribute
# !!! end_year is not the final year, but the end of the whole range (set +1 to final year)
def year_statistic(data, attribute_name, start_year, end_year, stat='ave'):
    timestamps = read_column(data, 'Timestamp')
    column = read_column(data, attribute_name)
    stamps = stamps_for_years_between(start_year, end_year)
    stats = []
    for i in range(len(stamps) - 1):
        year_column = []
        for j in range(len(timestamps)):
            if (int(stamps[i]) <= int(timestamps[j])) and (int(timestamps[j]) < int(stamps[i+1])):
                year_column = np.append(year_column, column[j])
        if stat == 'ave':
            year_statistic = np.average(year_column)
        if stat == 'std': 
            year_statistic = np.std(year_column)
        stats = np.append(stats, year_statistic)
    return stats

# CURRENTLY NOT USED
# forms condition for big_stories_in_year using averages and deviations values (or fixed value)
def obtain_conditions(averages, deviations):
    condition = np.multiply(deviations, 5) + averages
    #condition = np.multiply(averages, 5)  
    #condition = np.sqrt(averages) 
    #condition = np.multiply(np.ones(len(averages)), 3500)
    return condition   

# compare attribute values for a each year included in the year_stamps apart from the last one (which only speficies the end of the range) to the condition, if the attribute is greater, this is considered a 'big story', output number of big stories in each year
def big_stories_in_year(data, attribute_name, timestamps, year_stamps, condition):
    column = read_column(data, attribute_name)
    big_story = []
    for i in range(len(year_stamps)-1):
        year_big_story = 0
        for j in range(len(column)):
            if (int(year_stamps[i]) <= int(timestamps[j])) and \
               (int(timestamps[j]) < int(year_stamps[i+1])):
                if column[j] >= condition[i]:
                    year_big_story += 1 
        big_story = np.append(big_story, year_big_story)
    return big_story

# polynomial fit of set order using all but the last entry outputs the expected value for the last entry
def extrapolate_last_year(years, values):
    order = 1
    fit = np.polyfit(years[:-1], values[:-1], order)
    poly = np.poly1d(fit)
    return poly(years[-1])           

def big_stories(file_name, attribute_name):
    # Specification of the year range and data initialization
    start_year = 2015
    end_year = 2021 # not the final year, but the end of the time range (+1 to final year)
    year_range = np.arange(start_year, end_year)
    data = read_file(file_name)
    timestamps = read_column(data, 'Timestamp')
    averages = year_statistic(data, attribute_name, start_year, end_year, 'ave')
    deviations = year_statistic(data, attribute_name, start_year, end_year, 'std')
    year_stamps = stamps_for_years_between(start_year, end_year)
    
    # Linear extrapolation of average and deviation for 2020 from data 2015-2019
    expected_average = extrapolate_last_year(year_range, averages)
    new_averages = averages.copy()
    #new_averages[-1] = expected_average
    expected_deviation = extrapolate_last_year(year_range, deviations)
    new_deviations = deviations.copy()
    #new_deviations[-1] = expected_deviation
    
    # Forming condition for 'Big Story' (function obtain_conditions is also available)
    condition = np.multiply(new_deviations, 5) + new_averages  
    big_stories = big_stories_in_year(data, attribute_name, timestamps, year_stamps, condition)
    print('Using tweet %s from %s' % (attribute_name, file_name))
    print('{:>8} {:>10} {:>10} {:>10} {:>10}'.format(
        'Year','Average','StanDev','Conditn','BgStory'))
    for k in range(len(year_range)):
        print('{:8.0f} {:10.2f} {:10.2f} {:10.2f} {:8.0f}'.format(
            year_range[k], averages[k], deviations[k], condition[k], big_stories[k]))
    print('Extrapolating, the average in %s should be %.2f' % (end_year-1, expected_average))
    
    # Data plotting
    time_plot_column(data, attribute_name)
    plot_lines(year_stamps, averages, 'r', 'Average')
    plot_lines(year_stamps, (averages + deviations), 'b', 'Avg + Std')
    plot_lines(year_stamps, condition, 'g', 'Condition')
    plt.hlines(expected_average, year_stamps[-2], year_stamps[-1], 
               colors = 'orange', label = 'Expected avg', zorder=10)
    plt.title(file_name)
    plt.xlabel('Year')
    plt.ylabel(attribute_name)
    plt.xticks(year_stamps, year_range, ha = 'left')
    plt.legend()
    plt.show()

print('Select source or leave blank for default\n', source)
given_source_name = str(input('Enter source: '))
print('Select attribute or leave blank for default\n', attribute)
given_attribute_name = str(input('Enter attribute: '))
source_name, attribute_name = file_path_check(given_source_name, given_attribute_name)
big_stories(source_name, attribute_name)
