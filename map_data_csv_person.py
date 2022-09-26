import json
import os
from os import walk
from os import path
from pathlib import Path
import yaml
from yaml.loader import SafeLoader


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

    idx = "zz"
    for record in records:
        counter = 1
        id = record["Unique_Constituents_ID"]
        if (id.strip() == ""):
                continue 
        fname = b_mapped + '/' + id + '.json'
        
 

        # check if person file exists - if yes, update
        if (os.path.isfile(fname)):
               
            mapped_data_additional_record = map_data_func.exhibition_person(record,template)

            # get exhibition data
            data = json.loads(mapped_data_additional_record)
            if "exhibitions" in data.keys():
                # get exhibition
                exhibition = data["exhibitions"][0]
                
                # now insert into original file for the exhibition
                # open file 
                filepath = "./" + b_mapped + "/"+ str(id) + ".json"
               
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    data["exhibitions"].append(exhibition)
                    f.close()
                   
                    with open(filepath, 'w') as f:
                        f.write(json.dumps(data, indent=2))
                    f.close() 
                
  
        else:
            id = record["Unique_Constituents_ID"]
            if (id.strip() == ""):
                continue 
            print("person file created:" + id)
            mapped_data = map_data_func.exhibition_person(record,template)
            map_data_func.save_file(mapped_data, b_mapped, id)
        

