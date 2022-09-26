
local la_base_uri = 'http://localhost:3010/api/';

local person_id = la_base_uri + 'person/' + std.extVar('id');

local birth_date = std.extVar('birth_date');
local death_date = std.extVar('death_date');
local person_bio = std.extVar('person_bio');
local viaf = std.extVar('person_wiki_id');
local wikidata = std.extVar('person_wiki_id');
local ulan = std.extVar('person_ulan_id');
local display_name = std.extVar('person_display_name');
local person_name = std.extVar('person_name');
local person_role = std.extVar('person_role');

// exhibition
local exhibition_label = std.extVar('exhibition_label');
local exhibition_id = la_base_uri + 'exhibition/' + std.extVar('exhibition_id');

local exhibition_org = std.extVar('exhibition_org');
local exhibition_org_id = la_base_uri + 'group/id/1';
//  date
local date_begin = std.extVar('startdate');
local date_end = std.extVar('enddate');
local date_label = date_begin + ' - ' + date_end;

//  place
local place_id = la_base_uri + 'place/';
local place_label = std.extVar('place_label');

//=================================

{
  id: person_id,
  label: display_name,
  identifiers: {
    display_name: display_name,
    alphsort_name: person_name,
    ulan: ulan,
    wikidata: wikidata,
    viaf: viaf,
  },
  birth_date: birth_date,
  death_date: death_date,
  description: person_bio,

  exhibitions: [{
    exhibition: {
      id: exhibition_id,
      label: exhibition_label,
      date: {
        begin: date_begin,
        end: date_end,
        label: date_label,
      },
      place: {
        id: place_id,
        label: place_label,
      },
      org: {
        id: exhibition_org_id,
        label: exhibition_org,
      },
      role: person_role
    },
  }],
}
