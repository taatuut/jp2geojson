# test_exme.py

# python3 test_exme.py

# python3 -m pip install glymur
# ls /usr/local/lib/python3.9/site-packages/glymur/data/
# goodstuff.j2k   heliov.jpx      nemo.jp2
# cp /usr/local/lib/python3.9/site-packages/glymur/data/*.j* ./JPEG2000/

# Tested on MacOS with Python 3.9 and PyPy 3.8 with glymur and pyyaml installed, borrowed the sample files from glymur

import exme

# TODO: change to using dir and output arguments like in photos2geojson main.py

#j = ['./JPEG2000//heliov.jpx']
j = ['./JPEG2000/goodstuff.j2k','./JPEG2000//heliov.jpx','./JPEG2000/nemo.jp2','./JPEG2000/sample1.jp2']
for i in j:
    exme.jp2Metadata(i)

# Expected result:
# For every input file a .txt and .json file in ./Output with either raw jp2 data and converted to json