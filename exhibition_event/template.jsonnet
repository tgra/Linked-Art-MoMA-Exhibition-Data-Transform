
local la_base_uri = 'https://linkedart.example.com/';


local exhibition_label = std.extVar('label');
local exhibition_id = la_base_uri + "exhibition/" + std.extVar('id');
local exhibition_type_id = "http://vocab.getty.edu/aat/300054766";
local exhibition_type_label = "Exhibiting";
local exhibition_url = std.extVar("exhibition_url");

local exhibition_org = std.extVar('exhibition_org');
local exhibition_org_id = la_base_uri + 'group/id/1';
//  date
local date_begin = std.extVar('startdate');
local date_end = std.extVar('enddate');
local date_label = date_begin + "-" + date_end;

//  place
local place_id = la_base_uri + "place/";
local place_label = std.extVar('place_label');

// identifiers
local primary_name = std.extVar('primary_name');

// person
local viaf  = std.extVar('person_wiki_id');
local wikidata  = std.extVar('person_wiki_id');
local ulan  = std.extVar('person_ulan_id');
local display_name = std.extVar("person_display_name");
local person_role = std.extVar("person_role");
//=================================

{
  id: exhibition_id,
  label: exhibition_label,
  type: "Activity",
  classified_as_type: [
    {
      id: exhibition_type_id, 
      _label : exhibition_type_label,
    }
   
    ],
  identified_by : {
    "primary_name": {
    "_label": primary_name,
    "type_id": 300404670
    }
  
  }
    ,
    timespan : {
      begin_of_begin: date_begin,
      end_of_end: date_end,
    },
    location: [{
      id: place_id,
      _label: place_label,
      type: "Place",

    }],
    carried_out_by:[
      {
      id : exhibition_org_id,
      type : "Group",
      _label : exhibition_org,
    }
    ],

persons  : [{
  person:  {
  role: person_role,
  identified_by: {
  viaf: viaf,
  wikidata: wikidata,
  ulan: ulan}
  ,
  name: {
    display_name: display_name,}
  
  }
  }
],
    
}