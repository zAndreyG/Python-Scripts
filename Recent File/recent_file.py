import glob
import os

list_of_files = glob.glob('D:/Users/CSV_Files/*.csv') # * means all, if need a specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print (str(latest_file))