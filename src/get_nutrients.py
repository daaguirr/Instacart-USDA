import sys
import time

import requests
import pandas as pd
import os
import numpy as np

name_dicc = {
    '208': 'Energy (Kcal)',
    '203': 'Protein(g)',
    '204': 'Total Lipid (g)',
    '255': 'Water (g)',
    '307': 'Sodium(mg)',
    '269': 'Total Sugar(g)',
    '291': 'Fiber(g)',
    '301': 'Calcium(mg)',
    '303': 'Iron (mg)',
}

path = os.getcwd()
link = pd.read_csv(os.path.join(path, 'link.csv'), sep=",", dtype={'ndbno': object})

numbers = link['ndbno'].tolist()


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


it = chunks(numbers, 25)
arr = []
g100 = []
for _i, chunk in enumerate(it):
    print(f"Progress: {_i*100/(len(numbers)/25) :.2f}%")
    response = {
        'api_key': 'API',
        'ndbno': chunk,
        'format': 'json',
    }

    req = requests.get('https://api.nal.usda.gov/ndb/V2/reports', response)

    for fd in req.json()['foods']:
        if 'food' not in fd:
            continue
        food = fd['food']
        name = food['desc']['name']
        ndbno = food['desc']['ndbno']
        nut_dicc = {
            '208': np.nan,
            '203': np.nan,
            '204': np.nan,
            '255': np.nan,
            '307': np.nan,
            '269': np.nan,
            '291': np.nan,
            '301': np.nan,
            '303': np.nan,
        }

        ver = True
        for nutrient in food['nutrients']:
            if nutrient['nutrient_id'] in nut_dicc and \
                    ('measures' not in nutrient or len(nutrient['measures']) == 0 or nutrient['measures'] == [None]):
                ver = False
        if not ver:
            g100 += [ndbno]
            print(ndbno)

        for nutrient in food['nutrients']:
            if nutrient['nutrient_id'] in nut_dicc:
                try:
                    if ver:
                        measure = nutrient['measures'][0]
                        nut_dicc[nutrient['nutrient_id']] = float(measure['value'])
                    else:
                        nut_dicc[nutrient['nutrient_id']] = float(nutrient['value'])
                except:
                    print(ndbno)
                    sys.exit(1)

        ans = {'NDB_No': ndbno, 'USDA Name': name}
        for key, value in nut_dicc.items():
            ans[name_dicc[key]] = value
        arr += [ans]
    time.sleep(1)

df = pd.DataFrame(arr)
df = df[['NDB_No', 'USDA Name', 'Energy (Kcal)', 'Total Sugar(g)', 'Total Lipid (g)', 'Water (g)', 'Protein(g)',
         'Sodium(mg)', 'Fiber(g)', 'Calcium(mg)', 'Iron (mg)', ]]
df.to_csv(os.path.join(path, 'nutrient_linkage.csv'), encoding='utf-8', index=False)

print(len(g100))
print(g100)
