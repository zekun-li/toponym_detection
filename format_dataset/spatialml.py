import os 
import sys 
import json
import glob
from bs4 import BeautifulSoup

import pdb 

dataset_dir = '/data4/zekun/toponym_detection/spatialml/mitre_spatialml_v1/data/'
file_list = glob.glob(os.path.join(dataset_dir,'*.sgm.gaz-deref'))
file_list = sorted(file_list)

pdb.set_trace()

print(len(file_list))
for file_path in file_list:
    
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
    pdb.set_trace()