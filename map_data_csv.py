import json
import os
from os import walk
from pathlib import Path
from re import M
import yaml
from yaml.loader import SafeLoader

import pandas as pd

import csv

# mapping functions in local dir
import map_data_func

# settings.py in local dir
import settings
[objtype, config_file, template] = settings.map_data()

# ===============================================
# READ IN CONFIG

with open(config_file) as f:
    data = yaml.load(f, Loader=SafeLoader)
    config = data[1]

directory = config["directory"]
a_collection = directory + config["a_collection"] # dir to store collection data files
b_mapped = directory + config["b_mapped"] # dir to store mapped data
template = Path(template).read_text() # jsonnet template for intermediate JSON data file

## ===============================================
# ITERATE OVER FILES IN COLLECTION DATA DIR

files = []
for (dirpath, dirnames, filenames) in walk(a_collection):
    for filename in filenames:
        if filename.endswith('.csv'):
            files.append(filename)
    break

files.sort()

# remove BOM
for file in files:
    filepath = a_collection + '/' + file
    # open file 
    s = open(filepath, mode='r', encoding='utf-8-sig').read()
    # write to file 
    open(filepath, mode='w', encoding='utf-8').write(s)


# read in file 
for file in files:
    filename = os.path.basename(file)
    print(filename)  
    # open file 
    filepath = a_collection + '/' + file
    records = csv.DictReader(open(filepath, mode='r',encoding='utf-8'))
    
   
    mapped_data = None

    id = ""
    for record in records:
        counter = 1

        if record["Unique_ExhibitionsEvents_ID"] == id:
            
            
            mapped_data_additional_record = map_data_func.exhibition(record,template)

            # get person data
            data = json.loads(mapped_data_additional_record)
            if "persons" in data.keys():
                # get persons
                person = data["persons"][0]
                
                # now insert into original file for the exhibition
                # open file 
                filepath = "./" + b_mapped + "/"+ str(id) + ".json"
               
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    data["persons"].append(person)
                    f.close()
                   
                    with open(filepath, 'w') as f:
                        f.write(json.dumps(data, indent=2))
                    f.close() 
                
                
                
            
        else:
            id = record["Unique_ExhibitionsEvents_ID"]
            print("primary file:" + id)
            mapped_data = map_data_func.exhibition(record,template)
            
            map_data_func.save_file(mapped_data, b_mapped, id)
        

