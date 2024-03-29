
import cromulent 
from cromulent.model import factory, Group, DigitalObject, TimeSpan
from cromulent.vocab import Event, Birth, Death, AttributeAssignment, Exhibition, Type, Set, LinguisticObject, Name, InformationObject, Creation, VisualItem, Identifier, Production, HumanMadeObject, Dimension, MeasurementUnit, TimeSpan, Place, Person, Language, DigitalService

import json
# ==========================



def person_pattern(data, globalvars):

    ulan_uri = "http://vocab.getty.edu/page/ulan/"
    viaf_uri  = "https://viaf.org/viaf/"
    wikidata_uri = "https://www.wikidata.org/wiki/"

    id = data["id"]
    label = data["label"]

    person = Person(ident=id, label=label)

    person.identified_by = Name(label=label)
    person.identified_by = Name(label=data["identifiers"]["alphsort_name"])
    person.identified_by = Identifier(ident=ulan_uri + data["identifiers"]["ulan"], label="ULAN Identifier")
    person.identified_by = Identifier(ident=viaf_uri + data["identifiers"]["viaf"], label="VIAF Identifier")
    person.identified_by = Identifier(ident=wikidata_uri + data["identifiers"]["wikidata"], label="Wikidata Identifier")


    birth = Birth(label = "Birth")
    timespan = TimeSpan(label= label + " Birth timespan")
    timespan.begin_of_the_begin = data["birth_date"]
    timespan.end_of_the_end = data["birth_date"]
    birth.timespan = timespan
    person.born = birth

    death = Death(label = "Death")
    timespan = TimeSpan(label= label + " Death timespan")
    timespan.begin_of_the_begin = data["death_date"]
    timespan.end_of_the_end = data["death_date"]
    death.timespan = timespan
    person.died = death

    if data["description"] != "":
        lo = LinguisticObject()
        lo.content = data["description"]
        lo.classified_as = Type(ident="http://vocab.getty.edu/aat/300435422", label="Biography Statement")
        person.referred_to_by = lo
        
    return person

def timespan_pattern(data):

    timespan = TimeSpan(ident="", label=data["label"])
    timespan.begin_of_the_begin = data["begin"]
    timespan.end_of_the_end = data["end"]
    return timespan

def place_pattern(data, globalvars):

    place = Place(label=data["label"])
    place.classified_as = type_pattern(300005768, globalvars)

    return place

def exhibition_person_pattern(data,globalvars):

    person = person_pattern(data, globalvars)

    set = Set(label="Exhibitions")
    for exhibition in data["exhibitions"]:
        if "exhibition" in exhibition:

            d = exhibition["exhibition"]

            ex = Event(ident=d["id"],label=d["label"])
            ex.timespan = timespan_pattern(d["date"])
            
            ex.took_place_at = place_pattern(d["place"],globalvars)
            set.about = ex
            
    
    
   
    aa = AttributeAssignment()
    aa.involved = set
    person.assigned_by = aa

    return person




def exhibition_pattern(data, globalvars):

    # identifier and label
    type_id = 300054766
    
    
    exhibition = Exhibition(ident= data["id"], label=data["label"])

    # classified_as
    
   # identifiers
   
    if "primary_name" in data["identified_by"].keys():
        exhibition.identified_by = name_pattern(data["identified_by"]["primary_name"], globalvars)

    
    # timespan
    data_time = data["timespan"]
    timespan = TimeSpan(ident="", label="")
    timespan.begin_of_the_begin = data_time["begin_of_begin"]
    timespan.end_of_the_end = data_time["end_of_end"]

    exhibition.timespan = timespan

    place = Place(label=data["location"][0]["_label"])
    place.classified_as = type_pattern(300005768, globalvars)
    exhibition.took_place_at = place

    roles = []
    for person in data["persons"]:
        person_role = person["person"]["role"]
        if person_role not in roles:
            roles.append(person_role)

    aa = AttributeAssignment()
    role_list = []
    for role in roles:
        
        set = Set(label=role)
        person_list = []
        for person in data["persons"]:
            
            person_role = person["person"]["role"]
            if (person_role == role):
                display_name = person["person"]["name"]["display_name"] 
                person_id = person["person"]["id"]
                person = Person(label=display_name, ident=person_id)
                person_list.append(person)
        set.about = person_list
        role_list.append(set)        
    aa.involved = role_list
    exhibition.part = aa

    # carried out by 
    if "carried_out_by" in data:
        label = data["carried_out_by"][0]["_label"]
        grp = Group(label=label)
        grp.classified_as = Type(ident="http://vocab.getty.edu/aat/300312281", label="Museum")
        exhibition.carried_out_by = grp
         

    return exhibition




def set_pattern(data,globalvars):
    
    types   = globalvars['types']
    uris     = globalvars['uris']

    # identifier and label
    id = data["type_id"]
    label = data["_label"]
    
    set = Set(ident= uris["aat"] + str(id), label=label)

    # classified_as
    set.classified_as = type_pattern(id, globalvars)

    # subject_of web page
    if "homepage" in data["subject_of"][0]:
        set.subject_of = web_page_pattern(data["subject_of"][0]["homepage"], globalvars)

    # subject_of iiif
    set.subject_of = iiif_pattern(data["subject_of"][0]["iiif"], globalvars)

   # identifiers
    if "name" in data["identified_by"]:
        set.identified_by = name_pattern(data["identified_by"]["name"], globalvars)

    if "pia-id" in data["identified_by"]:
        set.identified_by = identifier_pattern(
            data["identified_by"]["pia-id"], globalvars)

    if "sgv-signature" in data["identified_by"]:
        set.identified_by = identifier_pattern(
            data["identified_by"]["sgv-signature"], globalvars)

    if "description" in data:
        lo_type = Type(id= "http://vocab.getty.edu/aat/300435416", label="Description")
        lo_type.classified_as = Type(id="http://vocab.getty.edu/aat/300418049", label="Brief Text")
        lo = LinguisticObject(id="", content=data["description"])
        lo.classified_as = lo_type
        set.referred_to_by =  lo

    return set



def humanmadeobject_pattern(data, globalvars):

    types   = globalvars['types']
    uris     = globalvars['uris']

    # identifier and label
    id = data["type_id"]
    label = data["_label"]

    hmo = HumanMadeObject(ident=uris["aat"] + str(id), label=label)

    # classified_as
    hmo.classified_as = type_pattern(id, globalvars)

    # member_of collection
    hmo.member_of = collection_pattern(data, globalvars)

    # subject_of web page
    hmo.subject_of = web_page_pattern(data["subject_of"][0], globalvars)

    # subject_of iiif
    hmo.subject_of = iiif_pattern(data["subject_of"][1], globalvars)

    # not supported in cromulent
    # hmo_1.current_owner        = Group(ident="", label="")

    # production
    if "produced_by" in data:
        hmo.produced_by = produced_by_pattern(data["produced_by"], globalvars)

    # dimensions
    # no data available at moment

    # shows
    if "shows" in data and data["_label"] != "":
        hmo.shows = shows_pattern(data["shows"], globalvars)

    # representation

    # digital object
    id_digital_object = data["representation"][0]["digital_surrogate"]["id"]
    digital_object = DigitalObject(ident="", label="")
    digital_object.format = "image/jpeg"
    digital_object.access_point = DigitalObject(
        ident=id_digital_object, label='Image in full resolution')
    digital_object.classified_as = Type(
        id="http://vocab.getty.edu/aat/300215302", label="Digital Image")

    if "iiif_image_api" in data["representation"][0]:
        iiif_image_api = data["representation"][0]["iiif_image_api"]["id"]
        digital_object.digitally_available_via = digital_service_pattern(
            data, types, iiif_image_api)

    # visualitem
    label_visual_item = data["representation"][0]["digital_surrogate"]["_label"]
    visual_item = VisualItem(id="", label=label_visual_item)
    visual_item.digitally_shown_by = digital_object

    hmo.representation = visual_item

    # identifiers
    if "name" in data["identified_by"]:
        hmo.identified_by = name_pattern(data["identified_by"]["name"], globalvars)

    if "pia-id" in data["identified_by"]:
        hmo.identified_by = identifier_pattern(
            data["identified_by"]["pia-id"], globalvars)

    if "sgv-signature" in data["identified_by"]:
        hmo.identified_by = identifier_pattern(
            data["identified_by"]["sgv-signature"], globalvars)

    if "creator-assigned" in data["identified_by"]:
        hmo.identified_by = identifier_pattern(
            data["identified_by"]["creator-assigned"], globalvars)


    return hmo


def digital_object_pattern(data, globalvars):

    types   = globalvars['types']
    uris     = globalvars['uris']
   
    id = data["type_id"]
    label = data["_label"]

    # identifier and label
    digital_object = DigitalObject(ident=uris["aat"] + str(id), label=label)

    # classified_as
    digital_object.classified_as = type_pattern(id, globalvars)

    # member_of collection
    digital_object.member_of = collection_pattern(data, globalvars)

    # subject_of web page
    digital_object.subject_of = web_page_pattern(data["subject_of"][0], globalvars)

    # subject_of iiif
    digital_object.subject_of = iiif_pattern(data["subject_of"][1], globalvars)

    # not supported in cromulent
    # digital_object_1.current_owner        = Group(ident="", label="")

    # creation and production
    if "created_by" in data:
        digital_object.created_by = creation_pattern(data["created_by"], globalvars)

    # digitally_shows
    if "digitally_shows" in data and data["_label"] != "":
        digital_object.digitally_shows = digitally_shows_pattern(
            data["digitally_shows"], globalvars)

    # identifiers
    if "name" in data["identified_by"]:
        digital_object.identified_by = name_pattern(data["identified_by"]["name"], globalvars)

    if "pia-id" in data["identified_by"]:
        digital_object.identified_by = identifier_pattern(
            data["identified_by"]["pia-id"], globalvars)

    if "sgv-signature" in data["identified_by"]:
        digital_object.identified_by = identifier_pattern(
            data["identified_by"]["sgv-signature"], globalvars)

    if "creator-assigned" in data["identified_by"]:
        digital_object.identified_by = identifier_pattern(
            data["identified_by"]["creator-assigned"], globalvars)

    # access point
    if "access_point" in data:
        digital_object.access_point = DigitalObject(
            ident=data["access_point"]["id"], label=data["access_point"]["_label"])

    # digitally available via
    if "iiif_image_api" in data:
        digital_object.digitally_available_via = digital_service_pattern(
            data, globalvars, data["iiif_image_api"])

    return digital_object

# ==================================


def digital_service_pattern(data, types, iiif_image_api):

    digital_service = DigitalService(label="IIIF Image API", ident="")
    digital_service.format = "application/ld+json"
    digital_service.access_point = DigitalObject(ident=iiif_image_api)
    digital_service.conforms_to = InformationObject(
        ident="http://iiif.io/api/image/3/context.json")

    return digital_service


"""
    work_id = 300435443
    work = types.get(work_id)
    label = work.get("label")
    type.classified_as = Type(
        ident=uris["aat"] + str(work_id), label=label)
"""

def type_pattern(id, globalvars):
    
    types   = globalvars.get('types')
    uris     = globalvars.get("uris")
    selected_type = types.get(id)
    label = selected_type.get("label")
    
    type = Type(ident=uris["aat"] + str(id), label=label)


    return type


def collection_pattern(data, globalvars):

    id = data["member_of"][0]["id"]
    label = data["member_of"][0]["_label"]

    types   = globalvars.get('types')
    uris     = globalvars.get("uris")
    
    collection_type_id = 300025976
    

    collection = Set(ident=id, label=label)
    collection.classified_as = type_pattern(collection_type_id, globalvars)

    return collection


def web_page_pattern(data, globalvars):

    label = data["_label"]
    access_point_id = data["access_point_id"]
    web_page_type_id = 300264578

    digital_object = DigitalObject(ident="", label=label)
    digital_object.identified_by = Name(ident="", content=label)
    digital_object.format = "text/html"
    digital_object.access_point = DigitalObject(ident=access_point_id)
    digital_object.classified_as = type_pattern(web_page_type_id, globalvars)

    linguistic_object = LinguisticObject(ident="", label=label)
    linguistic_object.digitally_carried_by = digital_object

    return linguistic_object


def iiif_pattern(data, globalvars):

    label = data["_label"]
    access_point_id = data["access_point_id"]
    iiif_id = "http://iiif.io/api/presentation/3/context.json"

    digital_object = DigitalObject(ident="", label=label)
    digital_object.format = "application/ld+json"
    digital_object.access_point = DigitalObject(ident=access_point_id)
    digital_object.conforms_to = InformationObject(ident=iiif_id, label="")
    digital_object.identified_by = Name(ident="", label=label)

    linguistic_object = LinguisticObject(ident="", label=label)
    linguistic_object.digitally_carried_by = digital_object

    return linguistic_object


def negative_pattern(data, globalvars):

    label = data["_label"]
    negative_type_id = 300128343
    work_type_id = 300435443

    # negative
    hmo = HumanMadeObject(ident="", label=label)
    hmo.classified_as = type_pattern(negative_type_id, globalvars)
   
    # measurement dimension

    # width

    if "width" in data and data["width"] != "":
        width = Dimension(ident="", label="")
        width_type_id = 300055647
        width.classified_as = type_pattern(width_type_id,globalvars)
        width.value = data["width"]
        width.unit = MeasurementUnit(
            id=300379098, label="Centimetres")
        hmo.dimension = width
    # height

    if "height" in data and data["height"] != "":
        height = Dimension(ident="", label="")
        height_type_id = 300055644
        height.classified_as = type_pattern(height_type_id,globalvars)
        height.value = data["height"]
        height.unit = MeasurementUnit(
            label="Centimetres", id=300379098)
        hmo.dimension = height

    return hmo


def produced_by_pattern(data, globalvars):

    # production
    production = Production(ident="", label="")

    if "used" not in data or "produced_by_event" not in data["used"]:
        return []
        
   

    data_prod = data["used"]["produced_by_event"]

    # production timespan
    timespan = TimeSpan(ident="", label="")
    timespan.begin_of_the_begin = data_prod["begin"]
    timespan.end_of_the_end = data_prod["end"]

    if data_prod["display_title"] != "":
        name = Name(ident="", label="")
        name.content = data_prod["display_title"]
        name.classified_as = type_pattern(
            "http://vocab.getty.edu/aat/300404669", globalvars)
        timespan.identified_by = name

    production.timespan = timespan

    # production location
    for place in data_prod["location"]:
        if "id" in place and place["id"] != "":
            pl = Place(ident=place["id"], label=place["_label"])
            pl.identified_by = Identifier(
                ident=place["id"], label='local identifier')

            if place["geonames_id"] != "":
                pl.identified_by = Identifier(
                    ident=place["geonames_id"], label='geonames identifier')
            production.took_place_at = pl

    # production carried out by
    for person in data_prod["person"]:
        if person["id"] != "":
            production.carried_out_by = Person(
                ident=person["id"], label=person["_label"])
    return production


def creation_pattern(data, globalvars ):

    # production
    production = Production(ident="", label="")

    if "produced_by_event" not in data["used"]:
        return {}
    data_prod = data["used"]["produced_by_event"]

    # production timespan
    timespan = TimeSpan(ident="", label="")
    timespan.begin_of_the_begin = data_prod["begin"]
    timespan.end_of_the_end = data_prod["end"]

    if data_prod["display_title"] != "":
        name = Name(ident="", label="")
        name.content = data_prod["display_title"]
        name.classified_as = type_pattern(
            300404669, globalvars)
        timespan.identified_by = name

    production.timespan = timespan

    # production location
    if "location" in data_prod:
        for place in data_prod["location"]:
            if "id" in place and place["id"] != "":

                pl = Place(ident=place["id"], label=place["_label"])
                pl.identified_by = Identifier(
                    ident=place["id"], label='local identifier')

                if place["geonames_id"] != "":
                    pl.identified_by = Identifier(
                        ident=place["geonames_id"], label='geonames identifier')

                production.took_place_at = pl

    # production carried out by
    if "person" in data_prod:
        for person in data_prod["person"]:
            if person["id"] != "":
                production.carried_out_by = Person(
                    ident=person["id"], label=person["_label"])

    # negative
    negative = negative_pattern(data["used"], globalvars)
    negative.produced_by = production
    negative.shows = VisualItem(ident="", label=data["used"]["_label"])

    # creation
    creation = Creation(ident="", label=data["_label"])
    creation.used_specific_object = negative

    return creation


def shows_pattern(data, globalvars):

    label = data["_label"]

    visual_item = VisualItem(ident="", label=label)

    if "type_id" in data:
        visual_item.represents = type_pattern(data["type_id"], globalvars)

    return visual_item


def digitally_shows_pattern(data, globalvars):

    label = data["_label"]

    visual_item = VisualItem(ident="", label=label)

    if "type_id" in data:
        visual_item.represents_instance_of_type = type_pattern(
            data["type_id"], globalvars)

    return visual_item


def name_pattern(data, globalvars):

    uris = globalvars["uris"]
    types = globalvars["types"]

    label = data["_label"]
    if label =="":
        return NULL
    name = Name(ident="", label=label)

    name.classified_as = type_pattern(
        300404670, globalvars)

    if "language" in data:
        lang = data["language"]
        lang_id = lang.get("type_id")
        selected_type = types.get(lang_id) 
        label = selected_type.get('label')

        name.language = Language(
            ident=uris["aat"] + str(lang_id), label=label)

    return name


def identifier_pattern(data, globalvars):
    value = data["value"]
    type_id = data["type_id"]

   
    identifier = Identifier(content=value, ident="")
    identifier.classified_as = type_pattern(type_id, globalvars)

    return identifier
