import json
import _jsonnet

def save_file(data, dir, id):
    if data != "":
        mapped_data =  json.dumps(json.loads(data),indent=2)   
        # write intermediate json data format to file
        filepath = "./" + dir + "/"+ str(id) + ".json"
        f = open(filepath , "w")
        f.write(mapped_data)
        f.close() 
       


def reformatDate(date, char):
    
    date_arr = date.split(char)

    if len(date_arr) == 3:
        date = date_arr[2] + '-' + date_arr[1] + '-' + date_arr[0]
        return date
    return date

def exhibition_person(data,template):

    startdate = data["Startdate"]
    startdate = reformatDate(startdate, "/")

    enddate = data["EndDate"]
    enddate = reformatDate(enddate, "/")
    
    json_str = "{}"
    
    ext_vars = {
        "id"                : data["Unique_Constituents_ID"],
        "person_role"   : data["Constituent Role"],
        "person_name"   : data["AlphaSortName"],
        "person_display_name" : data["DisplayName"],
        "person_viaf_id"   : data["VIAFID"],
        "person_wiki_id"   : data["WikidataQID"],
        "person_ulan_id"   : data["ULANID"],
        "birth_date"        : data["TMSBirthYear"],
        "death_date"        : data["TMSDeathYear"],
        "person_bio"        : data["TMS DisplayBio"],

        "exhibition_label"  : data["Exhibition Title"],
        "exhibition_id"     : data["Unique_ExhibitionsEvents_ID"],
        "startdate"     : startdate,
        "enddate"       : enddate,
        "place_label"   : data["Exhibition Location/Address"],
        "exhibition_url": data["Exhibitions_Events_URL"],
        "exhibition_org" : data["ExhibitingInstitution"],

        
        }

    
    # iterate through ext_vars - if any values == None, replace with empty string
    for k , val in ext_vars.items():
        if val is None:
            ext_vars.update({k: ""})
    
    # use jsonnet to populate template with vars from ext_vars python dict
    json_str = _jsonnet.evaluate_snippet("snippet", template, ext_vars=ext_vars)

    if json_str != "":
        return json.dumps(json.loads(json_str),indent=2)
    else:
        return False


def exhibition(data,template):

    startdate = data["Startdate"]
    startdate = reformatDate(startdate, "/")

    enddate = data["EndDate"]
    enddate = reformatDate(enddate, "/")
    
    json_str = "{}"
    ext_vars = {
        "label"         : data["Exhibition Title"],
        "id"            : data["Unique_ExhibitionsEvents_ID"],
        "startdate"     : startdate,
        "enddate"       : enddate,
        "place_label"   : data["Exhibition Location/Address"],
        "primary_name"  : data["Exhibition Title"],
        "exhibition_url": data["Exhibitions_Events_URL"],

        "exhibition_org" : data["ExhibitingInstitution"],

        "person_role"   : data["Constituent Role"],
        "person_name"   : data["AlphaSortName"],
        "person_display_name" : data["DisplayName"],
        
        "person_viaf_id"   : data["VIAFID"],
        "person_wiki_id"   : data["WikidataQID"],
        "person_ulan_id"   : data["ULANID"],
        }

    
    # iterate through ext_vars - if any values == None, replace with empty string
    for k , val in ext_vars.items():
        if val is None:
            ext_vars.update({k: ""})
    
    # use jsonnet to populate template with vars from ext_vars python dict
    json_str = _jsonnet.evaluate_snippet("snippet", template, ext_vars=ext_vars)

    if json_str != "":
        return json.dumps(json.loads(json_str),indent=2)
    else:
        return False
    

def set(data,template):

# ext_vars dictionary holds vars from the collection data record
# In jsonnet it's not possible to test for the existence of an external variables dynamically, 
# therefore all variables need to be set, even if no data available
# ref https://jsonnet.org/ref/language.html

    ext_vars = {
        "id"            : data["id"],
        "label"         : data["attributes"]["label"],
        "signature"     : data["attributes"]["signature"],
        "salsah_id"     : data["attributes"]["salsah_id"],
        "description"     : data["attributes"]["description"]
        }

    
    # iterate through ext_vars - if any values == None, replace with empty string
    for k , val in ext_vars.items():
        if val is None:
            ext_vars.update({k: ""})
    
    # use jsonnet to populate template with vars from ext_vars python dict
    json_str = _jsonnet.evaluate_snippet("snippet", template, ext_vars=ext_vars)

    if json_str != "":
        return json.dumps(json.loads(json_str),indent=2)
    else:
        return False
       
'''
name:
map_data

purpose:
function to map collection data to intermediate JSON data file using jsonnet template

arguments:
- data - collection data json
- template - jsonnet template
- include_data - relevant included data in json from collection data  

'''

def images(data,template,include_data):

    if include_data is not None:
        [dates,places,collections] = include_data


# ext_vars dictionary holds vars from the collection data record
# In jsonnet it's not possible to test for the existence of an external variables dynamically, 
# therefore all variables need to be set, even if no data available
# ref https://jsonnet.org/ref/language.html

    ext_vars = {
        "id"            : data["id"],
        "title"         : data["attributes"]["title"],
        "base_path"     : data["attributes"]["base_path"],
        "signature"     : data["attributes"]["signature"],
        "oldnr"         : data["attributes"]["oldnr"],
        "salsah_id"     : data["attributes"]["salsah_id"],

        "date_start"    : "",
        "date_end"      : "",
        "date_display"  : "",
        "place_id"      : "",
        "geonames_id"   : "",
        "place_label"   : "",

        "collection_id": "",
        "collection_label"  : ""
        }

    # add collections
    try:
        collection_id = data["relationships"]["collections"]["data"][0]["id"]
        
        for collection in collections:
            if  collection["id"] == collection_id:
                ext_vars["collection_id"] = collection_id
                ext_vars["collection_label"] =   collection["attributes"]["label"]
    except:
        pass

    # add dates
    try:
        dates_id = data["relationships"]["date"]["data"]["id"]

        for date in dates:
            if  date["id"] == dates_id:
                ext_vars["date_start"] = date["attributes"]["date"]
                ext_vars["date_end"] =  date["attributes"]["end_date"]
                ext_vars["date_display"] = date["attributes"]["date_string"]
    except:
        pass

    # add place
    try:
        place_id = data["relationships"]["place"]["data"]["id"]

        for place in places:
            if  place["id"] == place_id:
                ext_vars["place_id"] = place["id"]
                ext_vars["geonames_id"] = "https://geonames.org/" + place["attributes"]["geonames_id"]
                ext_vars["place_label"] =  place["attributes"]["label"]
                
    except:
        pass
    
    # iterate through ext_vars - if any values == None, replace with empty string
    for k , val in ext_vars.items():
        if val is None:
            ext_vars.update({k: ""})
    
    # use jsonnet to populate template with vars from ext_vars python dict
    json_str = _jsonnet.evaluate_snippet("snippet", template, ext_vars=ext_vars)

    
    if json_str != "":
        return json.dumps(json.loads(json_str),indent=2)
       