#!/usr/bin/env -S uv run
import os
import sys
import csv
import json
import numpy as np
import scipy.io as sio
import nibabel as nib

brain_file = sys.argv[1]
elecsind_dir = sys.argv[2]
elecsrec_file = sys.argv[3]
elecsall_file = sys.argv[4]

###
MRI = nib.load(brain_file)
ras2tkras = MRI.header.get_vox2ras_tkr().dot(
        np.linalg.inv(MRI.header.get_vox2ras())) 

##
with open(elecsrec_file, 'r') as fn:
    csv_read = csv.reader(fn)
    eleclabels = np.array(list(csv_read), dtype=object)

##
json_elec_name = []
json_elec_coord = []
for lead_file in os.listdir(elecsind_dir):
    lead_json = json.load(open(os.path.join(elecsind_dir, lead_file), 'rb'))

    for pts in lead_json['points']:
        json_elec_name.append(pts["comments"][0]["text"])
        json_elec_coord.append([v for k,v in pts["coordinates"].items()])

json_elec_name = np.array(json_elec_name)
json_elec_coord = np.array(json_elec_coord, dtype=float)


## 
json_elec_name2 = []
json_elec_coord2 = []
for elbl in eleclabels[:,0]:
    print(elbl)
    json_elec_name2.append(json_elec_name[np.flatnonzero(json_elec_name == elbl)[0]])
    json_elec_coord2.append(json_elec_coord[np.flatnonzero(json_elec_name == elbl)[0]])
json_elec_name2 = np.array(json_elec_name2)
json_elec_coord2 = np.array(json_elec_coord2)
json_elec_coord2 = np.concatenate(
        (json_elec_coord2, np.ones((len(json_elec_coord2),1))), axis=1)


##
json_elec_coord_tkras = ras2tkras.dot(json_elec_coord2.T).T[:, :3]

##




##
sio.savemat(elecsall_file, {"eleclabels": eleclabels, "elecmatrix": json_elec_coord_tkras})
