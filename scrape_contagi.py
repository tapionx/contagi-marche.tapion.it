import datetime
import json

import requests

# https://www.regione.marche.it/Regione-Utile/Salute/Coronavirus/Report-contagiati-per-Comune

url = "https://www.regione.marche.it/DesktopModules/Covid19Stat/WSGetStatComu.ashx/GetPersonData?giornoScelto="
date = start_date = datetime.datetime(2021, 1, 1)
now = datetime.datetime.now()

DATA_FILENAME = "www/contagi_marche.json"


try:
    with open(DATA_FILENAME, "r") as f:
        dataset = json.loads(f.read())
        existing_dates = [x[0] for x in list(dataset.items())[0][1]]
except Exception as e:
    print(str(e))
    dataset = {}
    existing_dates = []

while now > date:
    date_str = date.strftime("%d/%m/%Y")
    if date_str in existing_dates:
        date += datetime.timedelta(days=1)
        continue
    r = requests.get(url + date_str)
    data = r.json()
    for city in data.get('data', []):
        city_name = city[0]
        quarantine_count = city[3]
        cases_count = city[4]
        if not city_name in dataset:
            dataset[city_name] = []
        dataset[city_name].append((date_str, cases_count, quarantine_count))
        #print(f"{date_str},{cases_count},{quarantine_count}")
    print(date)
    date += datetime.timedelta(days=1)

with open(DATA_FILENAME, "w") as f:
    f.write(json.dumps(dataset))

#print(r.json())

