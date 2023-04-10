import os 
import sys 
import json
import glob
from bs4 import BeautifulSoup

import pdb 


file_path = '../lgl/lgl.xml'
out_file_path = '../lgl/lgl.json'

with open(file_path, 'r') as f:
    soup = BeautifulSoup(f, "html.parser")

count_nongaz = 0 
ret_dict_list = []
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
        else:
            count_nongaz += 1 

        ret_dict['toponyms'].append(topo_dict) 

    ret_dict_list.append(ret_dict) 

print('count_nongaz:', count_nongaz)

with open(out_file_path, 'w',  encoding='utf8') as f:
    json.dump(ret_dict_list, f, indent = 2, ensure_ascii = False)
        

