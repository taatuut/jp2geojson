# test_exme.py

# python3 test_exme.py

# python3 -m pip install glymur
# ls /usr/local/lib/python3.9/site-packages/glymur/data/
# goodstuff.j2k   heliov.jpx      nemo.jp2
# cp /usr/local/lib/python3.9/site-packages/glymur/data/*.j* ./JPEG2000/

# Tested on MacOS with Python 3.9 and PyPy 3.8 with glymur and pyyaml installed

#  borrowed the sample files from glymur

# python3 test_main.py JPEG2000/ -o ./Results/geojson.json -l ./Results/map.html

import main

main.main()

# Expected result:
# In the output folder (use ./Results in this repo):
# - For every input file a .txt with raw JPEG 2000 data
# - and one (1) .json file for all images containing the metadata converted to geojson

# Then pickup with mongoimport or similar to ingest into MongoDB (Atlas)