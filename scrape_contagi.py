import datetime
import json

import requests

# https://www.regione.marche.it/Regione-Utile/Salute/Coronavirus/Report-contagiati-per-Comune

url = "https://www.regione.marche.it/DesktopModules/Covid19Stat/WSGetStatComu.ashx/GetPersonData?giornoScelto="
date = start_date = datetime.datetime(2021, 1, 1)
now = datetime.datetime.now()

dataset = {}

while now > date:
    date_str = date.strftime("%d/%m/%Y")
    r = requests.get(url + date_str)
    data = r.json()
    for city in data.get('data', []):
        city_name = city[0]
        cases_count = city[3]
        quarantine_count = city[4]
        if not city_name in dataset:
            dataset[city_name] = []
        dataset[city_name].append((date_str, cases_count, quarantine_count))
        #print(f"{date_str},{cases_count},{quarantine_count}")
    print(date)
    date += datetime.timedelta(days=1)

with open('www/contagi_marche.json', 'w') as f:
    f.write(json.dumps(dataset))

#print(r.json())

