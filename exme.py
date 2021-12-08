# exme.py

# python3 exme.py 

import glymur
import json
import os

def myconverter(o):
    return o.__str__()

def jp2Metadata(jp2file=None, path=None, options=None):
    jp2file = glymur.data.nemo() if jp2file is None else jp2file
    path = "./Results/" if path is None else path
    #COULDDO: check if path exists
    jp2name = jp2file.split('/')[-1]
    jp2 = glymur.Jp2k(jp2file)
    textfile = os.path.join(path,jp2name+".txt")
    jsonfile = os.path.join(path,jp2name+".json")
    dict1 = {}
    with open(textfile, 'w+') as tf:
        tf.write(str(jp2))
    # Need to step out and reopen to persist write?
    with open(textfile) as fh:  
        for line in fh:
            list = line.strip().split(':')
            key = list[0]
            val = list[1:] if len(list) > 1 else ""
            dict1[key] = " ".join(val).strip()

    feature_list = {
            "type": "Feature",
            "properties": {
                #"date": dict1['date'].isoformat() if dict1['date'] else '',
                "filename": dict1['File'] if dict1['File'] else '',
                #"location": dict1['location'] if dict1['location'] else '',
                "raw": dict1 if dict1 else ''
            },

            "geometry": {
                "type": "Point",
                "coordinates": [
                    #dict1['lon'],
                    #dict1['lat']
                    # using WL HQ coordinates as dummy
                    5.9956,51.1911
                ]
            }
        }

    with open(jsonfile, 'w') as jf:
        jf.write(json.dumps(feature_list, default = myconverter))
