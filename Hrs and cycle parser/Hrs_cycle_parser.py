import re
import pandas as pd


data = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# print(data)
all = []

for i in data.index:

    raw = data['Total'][i]
    try:
        hrs_raw = re.findall(r'([-,\d]+:[\d]*\sH)', raw)
        hrs_raw = hrs_raw[0].split(' H')[0]
    except IndexError:
        hrs_raw = ""
        print("-----------------")
        print(raw)

    try:
        cycle_raw = re.findall(r'([-\d]+\sC)', raw)
        cycle_raw = cycle_raw[0].split(' C')[0]
    except IndexError:
        cycle_raw = ""
        print("-----------------")
        print(raw)

    try:
        days_raw = re.findall(r'([-\d]+\sD)', raw)
        days_raw = days_raw[0].split(' D')[0]
    except IndexError:
        days_raw = ""
        print("-----------------")
        print(raw)

    all.append(([data['Serial No.'][i], data['Total'][i],hrs_raw, cycle_raw, days_raw]))

print(all)
processed_data = pd.DataFrame(all, columns=['Serial No.', 'Total','Hrs', 'Cycle', 'Days'])

processed_data.to_excel('processed_data.xlsx', index=False)

