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
    with open(jsonfile, 'w') as jf:
        jf.write(json.dumps(dict1, default = myconverter))
