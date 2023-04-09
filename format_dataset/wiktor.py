import os 
import sys 
import json
import glob
import csv
from bs4 import BeautifulSoup

import pdb 


file_path = '../wiktor/WikToR.xml'
out_file_path = '../wiktor/WikToR.json'
IF_WRITE_UNIQUE_NAME = False

with open(file_path, 'r') as f:
    soup = BeautifulSoup(f, "html.parser")

unique_names = []
formated_dict = {}
for page in soup.find_all('page'):

    page_title = page.find_all('pagetitle')[0].text  # not used
    toponym_name = page.find_all('toponymname')[0].text 
    text = page.find_all('text')[0].text  


    feature = page.find_all('feature')[0].text # not used
    url = page.find_all('url')[0].text # not used
    country = page.find_all('country')[0].text # not used

    lat = page.find_all('lat')[0].text 
    lon = page.find_all('lon')[0].text 

    toponyms = page.find_all('toponym')
    spans = []
    for toponym in toponyms:
        start_pos = int(toponym.start.text)
        end_pos = int(toponym.end.text)
        # print(text[start_pos: end_pos])
        spans.append((start_pos, end_pos))

    unique_names.append(toponym_name)

    cur_dict = {'text':text, 'feature':feature, 'url':url, 'country':country, 'lat':lat, 'lon':lon,
        'spans':spans}
    if toponym_name in formated_dict:
        formated_dict[toponym_name].append(cur_dict)
    else:
        formated_dict[toponym_name] = [cur_dict]

unique_names = set(unique_names) # list length: 5000, set length: 1886

with open(out_file_path, 'w') as f:
    json.dump(formated_dict, f, indent = 2)

if IF_WRITE_UNIQUE_NAME:
    with open('../wiktor/unique_names.csv', 'w') as f:
        # create CSV writer object
        writer = csv.writer(f)
        
        # write each string in the list as a separate row
        for n in unique_names:
            writer.writerow([n])



# pdb.set_trace()