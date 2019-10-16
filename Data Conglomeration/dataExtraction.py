import csv
import pandas as pd
import pdb

def extract_CSVs(category):
    label_list = timecard[category].unique()
    data_array = []
    for label in label_list:
        all_data = timecard[timecard[category] == label]
        cum_hours = all_data['hours'].cumsum()
        all_data.insert(7,'cum_hours',cum_hours)
        all_data[['date','hours','cum_hours']].to_csv('Files/' + category + 's/' + label + '.csv',index=False)





timecard = pd.read_csv('out.csv')
timecard.head()

categories = ['job', 'user', 'division']
for category in categories:
    extract_CSVs(category)
