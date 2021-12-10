# exme.py

# python3 exme.py 

import glymur
import json
import os
import re
import datetime

def getLocation(candidate):
    location = {
            "address": "OLV Kerk, AMersfoort, Utrecht, Netherlands"
        }
    return location

def getLon(candidate):
    lon = 5.3833
    reg_lon = re.compile("(.*)GPSLongitude>(.*)<(.*)")
    if bool(re.match(reg_lon, candidate)):
        result = reg_lon.search(candidate)
        lon = result.group(1).split("GPSLongitude>")[1].split("<")[0].split(".")[0].replace(",",".")
        lon = float(lon.strip(' "'))
    return lon

def getLat(candidate):
    lat = 52.15
    reg_lat = re.compile("(.*)GPSLatitude>(.*)<(.*)")
    if bool(re.match(reg_lat, candidate)):
        result = reg_lat.search(candidate)
        lat = result.group(1).split("GPSLatitude>")[1].split("<")[0].split(".")[0].replace(",",".")
        lat = float(lat.strip(' "'))
    return lat

def getTimestamp(candidate):
    ts = "1899-12-31T23:59:59"
    reg_ts = re.compile("(.*)GPSTimeStamp>(.*)<(.*)")
    if bool(re.match(reg_ts, candidate)):
        result = reg_ts.search(candidate)
        ts = result.group(1).split("GPSTimeStamp>")[1].split("<")[0].split(".")[0].replace(",",".")
    return ts

def myconverter(o):
    return o.__str__()

def textMe(file):
    dict = {}
    # NOTE: these tags end up in raw too but are not directly coming from file output...
    dict['location'] = ""
    dict['lon'] = 0
    dict['lat'] = 0
    dict['date'] = ""
    xmlbuffer = ""
    inbuffer = False
    with open(file) as fh:  
        for line in fh:
            if '<meta' in line or '<?xpacket begin' in line or inbuffer:
                xmlbuffer = xmlbuffer + line.strip()
                inbuffer = True
                if '</meta' in line or '<?xpacket end' in line:
                    inbuffer = False
            else:
                list = line.strip().split(':')
                key = list[0]
                val = list[1:] if len(list) > 1 else ""
                dict[key] = " ".join(val).strip()
            if len(xmlbuffer) > 0 and inbuffer == False:
                dict[key] = xmlbuffer
                # NOTE: many ways this will go wrong like multiple xmlbuffers overwriting legit info with default
                # gps info in other tags, gps info in other format... needs more investigation of the result text files
                dict['location'] = getLocation(xmlbuffer)
                dict['lon'] = getLon(xmlbuffer)
                dict['lat'] = getLat(xmlbuffer)
                dict['date'] = getTimestamp(xmlbuffer)
                xmlbuffer = ""
    return dict

class Node:
    def __init__(self, indented_line):
        self.children = []
        self.level = len(indented_line) - len(indented_line.lstrip())
        self.text = indented_line.strip()

    def add_children(self, nodes):
        childlevel = nodes[0].level
        while nodes:
            node = nodes.pop(0)
            if node.level == childlevel: # add node as a child
                self.children.append(node)
            elif node.level > childlevel: # add nodes as grandchildren of the last child
                nodes.insert(0,node)
                self.children[-1].add_children(nodes)
            elif node.level <= self.level: # this node is a sibling, no more children
                nodes.insert(0,node)
                return

    def as_dict(self):
        if len(self.children) > 1:
            return {self.text: [node.as_dict() for node in self.children]}
        elif len(self.children) == 1:
            return {self.text: self.children[0].as_dict()}
        else:
            return self.text

def treeMe(file):
    root = Node('root')
    with open(file) as fh:  
        root.add_children([Node(line) for line in fh])
        d = root.as_dict()['root']
        return d

def jp2Metadata(jp2file=None, path=None, options=None):
    jp2file = glymur.data.nemo() if jp2file is None else jp2file
    path = "./Results/" if path is None else path
    #COULDDO: check if path exists
    jp2name = jp2file.split('/')[-1]
    jp2 = glymur.Jp2k(jp2file)
    textfile = os.path.join(path,jp2name+".txt")
    jsonfile = os.path.join(path,jp2name+".json")
    with open(textfile, 'w+') as tf:
        tf.write(str(jp2))
    # Need to step out and reopen to persist write?
    #dict1 = treeMe(textfile)
    dict1 = textMe(textfile)
    feature_list = {
            "type": "Feature",
            "properties": {
                "date": dict1['date'],
                # NOTE: assuming tag File will always be in JPEG 2000 output
                "filename": dict1['File'] if 'File' in dict1 else '',
                "location": dict1['location'],
                "raw": dict1 if dict1 else ''
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    # using OLV Amersfoort coordinates as dummy
                    dict1['lon'],
                    dict1['lat']
                ]
            }
        }

    with open(jsonfile, 'w') as jf:
        jf.write(json.dumps(feature_list, default = myconverter))
