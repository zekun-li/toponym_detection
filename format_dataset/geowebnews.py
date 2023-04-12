import os 
import sys 
import json
import glob
import csv
from bs4 import BeautifulSoup

import pdb 

IF_WRITE_UNIQUE_NAME = True
file_path = '../geowebnews/GWN.xml'
out_file_path = '../geowebnews/GWN.json'

with open(file_path, 'r') as f:
    soup = BeautifulSoup(f, "html.parser")

count_nongaz = 0 
count_gaz = 0
count_nogeocoord = 0
ret_dict_list = []
unique_names = []

for article in soup.find_all('article'):
    ret_dict = {}
    text = article.find_all('text')[0].text 
    toponyms = article.find_all('toponym')
    ret_dict['sentence'] = text 
    ret_dict['toponyms'] = []
    for toponym in toponyms:
        
        if toponym.latitude is None:
            count_nogeocoord += 1
            continue 
        
        start_pos = int(toponym.start.text)
        end_pos = int(toponym.end.text)
        phrase = toponym.extractedname.text

        lat = float(toponym.latitude.text)
        lon = float(toponym.longitude.text)

        topo_dict = {'text':phrase, 'start':start_pos, 'end':end_pos, 'lat':lat, 'lon':lon}

        geonameid = toponym.geonamesid.text
        

        if len(geonameid) != 0: 
            topo_dict['geoname_id'] = geonameid
            
            unique_names.append(phrase) # list length: 5000, set length: 1886

            count_gaz += 1
        else:
            count_nongaz += 1 

        ret_dict['toponyms'].append(topo_dict) 
        # pdb.set_trace()

    ret_dict_list.append(ret_dict) 

print('count_nongaz:', count_nongaz)
print('count_gaz:', count_gaz)
print('count_nogeocoord:', count_nogeocoord)


# count_nongaz: 200
# count_gaz: 2401
# count_nogeocoord: 4011



with open(out_file_path, 'w',  encoding='utf8') as f:
    json.dump(ret_dict_list, f, indent = 2, ensure_ascii = False)
        

unique_names = set(unique_names) # list length: 5000, set length: 1886

if IF_WRITE_UNIQUE_NAME:
    with open('../geowebnews/unique_names.csv', 'w') as f:
        # create CSV writer object
        writer = csv.writer(f)
        
        # write each string in the list as a separate row
        for n in unique_names:
            writer.writerow([n])

