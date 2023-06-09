import os 
import sys 
import json
import glob
import csv
from bs4 import BeautifulSoup

import pdb 

IF_WRITE_UNIQUE_NAME = True
file_path = '../lgl/lgl.xml'
out_file_path = '../lgl/lgl.json'

with open(file_path, 'r') as f:
    soup = BeautifulSoup(f, "html.parser")

count_nongaz = 0 
count_gaz = 0
ret_dict_list = []
unique_names = []
for article in soup.find_all('article'):
    ret_dict = {}
    text = article.find_all('text')[0].text 
    toponyms = article.find_all('toponym')
    ret_dict['sentence'] = text 
    ret_dict['toponyms'] = []
    for toponym in toponyms:
        
        
        start_pos = int(toponym.start.text)
        end_pos = int(toponym.end.text)
        phrase = toponym.phrase.text
        gaztag = toponym.gaztag

        topo_dict = {'text':phrase, 'start':start_pos, 'end':end_pos}
        if gaztag is not None:
            geonameid = gaztag.get('geonameid')

            flcass = gaztag.fclass.text 
            fcode = gaztag.fcode.text 
            lat = float(gaztag.lat.text)
            lon = float(gaztag.lon.text)
            if gaztag.country is not None:
                country_geonameid = gaztag.country.get('geonameid')
                country_name = gaztag.country.text 
            if gaztag.admin1 is not None:
                admin1_geonameid = gaztag.admin1.get('geonameid')
                admin1_name = gaztag.admin1.text

            topo_dict['geoname_id'] = geonameid
            topo_dict['lat'] = lat 
            topo_dict['lon'] = lon 
            unique_names.append(phrase) # list length: 5000, set length: 1886

            count_gaz += 1
        else:
            count_nongaz += 1 

        ret_dict['toponyms'].append(topo_dict) 

    ret_dict_list.append(ret_dict) 

print('count_nongaz:', count_nongaz)
print('count_gaz:', count_gaz)

# count_nongaz: 626
# gaz: 4462

with open(out_file_path, 'w',  encoding='utf8') as f:
    json.dump(ret_dict_list, f, indent = 2, ensure_ascii = False)
        

unique_names = set(unique_names) # list length: 5000, set length: 1886

if IF_WRITE_UNIQUE_NAME:
    with open('../lgl/unique_names.csv', 'w') as f:
        # create CSV writer object
        writer = csv.writer(f)
        
        # write each string in the list as a separate row
        for n in unique_names:
            writer.writerow([n])

