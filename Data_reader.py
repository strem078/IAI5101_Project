import os
import glob
from datetime import datetime
import numpy as np
import pandas as pd

path = "./Data/"
os.chdir(path)
result = glob.glob('CavityData_*.csv') # Find all data file CSVs
fileDates = {} # Create an empty dictionary. Keys will be the data date and values will be the file names
currentTime = datetime.now() # Get the current time
for i in range(len(result)):
    file = result[i].replace('CavityData_','').replace('.csv','') # Remove the extension and prefix text
    tempDate = datetime.strptime(file, "%Y-%m-%d") # Extract the dates from the file names
    fileDates[currentTime - tempDate] = result[i] # Find the time differences, store them in a dictionary

latestName = fileDates[min(fileDates.keys())]
print(latestName) # Get the filename
latest_data = pd.read_csv(".\\CavityData_2024-03-03.csv")
print(latest_data)