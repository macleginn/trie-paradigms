import os
import os.path
import json

from datetime import datetime
from multiprocessing import Pool

import pandas as pd

from Table import corpora2dict

dirpath = "/home/macleginn/bible-corpus/corpus"
path_arr = []

if os.path.exists('patharr.json'):
    with open('patharr.json', 'r') as inp:
        path_arr = json.load(inp)
else:
    for filename in os.listdir(dirpath):
        if not filename.endswith('txt'):
            continue
        filepath = os.path.join(dirpath, filename)
        chars = set()
        with open(filepath, 'r', encoding='utf-8') as inp:
            for line in inp:
                chars.update(line)
        print(f'{filename[:-4]:40}{len(chars):4}')
        if len(chars) < 500:
            path_arr.append(filepath)
    with open('patharr.json', 'w') as out:
        json.dump(path_arr, out, indent=2, ensure_ascii=False)

# Separate the pathlist into four chunks
# Feed them to a Pool.map; accumulate the result
result_dict = {
    'log_frequency': [],
    'entropy': [],
    'doculect': []
}
input_arr = sorted(path_arr)
start = datetime.now()
with Pool(4) as p:
    for i, data_dict in enumerate(p.map(corpora2dict, input_arr, len(input_arr)//4)):
        for k in data_dict:
            result_dict[k].extend(data_dict[k])
        if (i+1) % 100 == 0:
            print(f"Checkpoint {i+1}")
            d = pd.DataFrame(result_dict)
            d.to_csv("/home/macleginn/Analyses/bible-tables/csv/sample-all.csv", index=False)
d = pd.DataFrame(result_dict)
d.to_csv("/home/macleginn/Analyses/bible-tables/csv/sample-all.csv", index=False)
print(datetime.now()-start)
