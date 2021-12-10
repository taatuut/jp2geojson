# jp2geojson

Converting JPEG 2000 / JP2 metadata to geojson using Python.

# Inspiration

https://github.com/Visgean/photos2geojson

https://stackoverflow.com/questions/17858404/creating-a-tree-deeply-nested-dict-from-an-indented-text-file-in-python

NOTE: Tried pyyaml but the text output is not wellformed enough for that.

# Specifics

## XML

Using the following tags to check for start and end of XML block:

```
<meta>
...
</meta>

<?xpacket begin='﻿' id='someidstringhere'?>
...
<?xpacket end='w'?>
```

## GPS

Using the following tags to check for GPS information:

```
GPSLatitude
GPSLongitude
GPSTimeStamp
GPSMapDatum
```

Found so far:

```
<ns4:GPSLatitude>42,20.56N</ns4:GPSLatitude>
<ns4:GPSLongitude>71,5.29W</ns4:GPSLongitude>
<ns4:GPSTimeStamp>2013-02-09T19:47:53Z</ns4:GPSTimeStamp>
<ns4:GPSMapDatum>WGS-84</ns4:GPSMapDatum>
```

NOTE: not yet doing anything with GPSMapDatum.

NOTE: a result map html file based on leaflet.html can be created. It does show the markers but not the images as these cannot be previewed in the browser (?). Some code tp create default markers for images without GPS info, needs some more work.

# General

Test generated geojson online with http://geojson.io/

Use the following code to generate a requirements.txt file:

```
python3 -m pip install pipreqs
cd /path/to/jp2geojson
pipreqs . --force
```

More on pipreqs at https://github.com/bndr/pipreqs

(Note: don't use `pip freeze` for this purpose, because it saves all packages in the environment including those not needed in the current project)