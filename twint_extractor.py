import csv
import os
from datetime import datetime
from matplotlib.dates import ( 
    DateFormatter, AutoDateLocator, AutoDateFormatter, datestr2num 
)
import xlsxwriter

#take date in YYYY-MM-DD format and time in hh:mm:ss and convert into timestamp of int-minutes since 0001-01-01
def compress_datetime(date, time):
    date_num = datestr2num(data[0][3])
    timearr = data[0][4].split(":")
    time_num = (int(timearr[0])*60)+int(timearr[1])
    stamp = int((date_num*1440)+time_num)
    return stamp

file_path = input("Type CSV file name, omitting .csv: ")

with open("{}.csv".format(file_path), encoding="utf-8") as f:
    file = f.readlines()
    headers = file[0].split("\t")
    data = [line.split("\t") for line in file[1:]]
    
    #don't need all data from the file (just id/timestamp/username/replies/retweets/likes)
    con_data = [[item[0], compress_datetime(item[3], item[4]), item[7], int(item[15]), int(item[16]), int(item[17])] for item in data]

#finally, write extracted data neatly into an Excel (.xlsx) file
workbook = xlsxwriter.Workbook("{}_data.xlsx".format(file_path))
worksheet = workbook.add_worksheet()
        
row = 0
col = 0

#header block
worksheet.write(row, col, "Tweet ID")
worksheet.write(row, col + 1, "Timestamp")
worksheet.write(row, col + 2, "Username")
worksheet.write(row, col + 3, "Reply no.")
worksheet.write(row, col + 4, "Retweets")
worksheet.write(row, col + 5, "Likes")
row += 1
    
for dehyd, datetime, user, replies, retweets, likes in con_data:
    worksheet.write(row, col, dehyd)
    worksheet.write(row, col + 1, datetime)
    worksheet.write(row, col + 2, user)
    worksheet.write(row, col + 3, replies)
    worksheet.write(row, col + 4, retweets)
    worksheet.write(row, col + 5, likes)
    row += 1
    
workbook.close()