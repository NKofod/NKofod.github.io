import requests
import json 
import random 
import time 

presidential_national_vote_url = "https://www.politico.com/election-data/results__2024-11-05__collections__2024-11-05-collection-president__summaries/data.json"
presidential_county_base_url_prefix = "https://www.politico.com/election-data/results__2024-11-05__contests__ap:" 
presidential_national_vote_url_suffix = ":0__counties/data.json"


with open("us_states.json", "r") as infile:
    national_feature_map = json.load(infile)
with open("candidate_ids.json", "r") as infile:
    candidates = json.load(infile)
with open("county_feature_list.json", "r") as infile:
    county_feature_map = json.load(infile)




v_request = requests.get(presidential_national_vote_url)
v_cont = v_request.content
v_dict = json.loads(v_cont)


for contest in v_dict["contests"]:
    tmp_id = contest["id"][3:5]
    harris = 0 
    trump = 0 
    third_party = 0 
    progress = contest['progress']['pct']
    for result in contest['results']:
        if candidates[result['id']] == 'Donald Trump': 
            trump += result['votes'] 
        elif candidates[result['id']] == 'Kamala Harris': 
            harris += result['votes']
        else: 
            third_party += result['votes']
    if harris+trump+third_party != 0:
        harris = harris/(harris+trump+third_party)
        trump = trump/(harris+trump+third_party)
        third_party = third_party/(harris+trump+third_party)
        harris *= 100
        trump *= 100
        third_party *= 100
    for i in national_feature_map['features']:
        if i['id'] == tmp_id:
            tmp_property_dict = i['properties']
            tmp_property_dict["harris"] = f"{harris:2.2f}"
            tmp_property_dict["trump"] = f"{trump:2.2f}"
            tmp_property_dict["third_party"] = f"{third_party:2.2f}"
            tmp_property_dict["progress"] = f"{progress:2.2f}"
            tmp_property_dict["margin"] = f"{harris - trump:2.2f}"
            #tmp_property_dict["margin"] = random.randint(-15,15)
            i["properties"] = tmp_property_dict
with open("us_states.js", "w") as outfile:
    outfile.write(f"var statesData = {json.dumps(national_feature_map)}")

with open(f"us_states_{time.time():.0f}.json", "w") as outfile:
			json.dump(national_feature_map, outfile)

for feature in national_feature_map['features']:
    state_request = requests.get(f"{presidential_county_base_url_prefix}{feature['id']}{presidential_national_vote_url_suffix}")
    state_content = state_request.content
    state_json = json.loads(state_content)
    for contest in state_json["counties"]:
        tmp_id = str(int(contest["id"]))
        #print(tmp_id)
        harris = 0 
        trump = 0 
        third_party = 0 
        progress = contest['progress']['pct']
        for result in contest['results']:
            if candidates[result['id']] == 'Donald Trump': 
                trump += result['votes'] 
            elif candidates[result['id']] == 'Kamala Harris': 
                harris += result['votes']
            else: 
                third_party += result['votes']
        if harris+trump+third_party != 0:
            harris = harris/(harris+trump+third_party)
            trump = trump/(harris+trump+third_party)
            third_party = third_party/(harris+trump+third_party)
            harris *= 100
            trump *= 100
            third_party *= 100
        for i in county_feature_map['features']:
            if i['id'] == tmp_id:
                tmp_property_dict = i['properties']
                tmp_property_dict["state"] = feature["properties"]["name"]
                tmp_property_dict["harris"] = f"{harris:2.2f}"
                tmp_property_dict["trump"] = f"{trump:2.2f}"
                tmp_property_dict["third_party"] = f"{third_party:2.2f}"
                tmp_property_dict["progress"] = f"{progress:2.2f}"
                tmp_property_dict["margin"] = f"{harris - trump:2.2f}"
                # tmp_property_dict["margin"] = random.randint(-15,15)
                i["properties"] = tmp_property_dict

with open("us_counties.js", "w") as outfile:
    outfile.write(f"var countyData = {json.dumps(county_feature_map)}")


with open(f"us_counties_{time.time():.0f}.json", "w") as outfile:
			json.dump(county_feature_map, outfile)
