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

# exiftool
Assumes exiftool, jq

Open terminal in folder `jp2geojson`

First text with:

`exiftool JPEG2000/ > Results/data.txt`

`exiftool -json JPEG2000/ > Results/data.json`

`exiftool -json -g -struct -r /Users/emilzegers/Dropbox/Bleia/DataFit/waterschaprivierenland.nl/ > Results/waterschaprivierenland.nl.json`

`exiftool -json -g -struct -r JPEG2000 > Results/JPEG2000.json`

`exiftool -json -g -struct -r ~/Downloads > Results/Downloads.json`

Prefer `-g` over `-G4`.

For verbose output, add `-v` Output size for json goes from 569 kb to 45 Mb. Quite CPU intensive.

NOTE: cannot combine verbose with json output as using verbose ignores most other options, see https://exiftool.org/exiftool_pod.html Using -v0 is not an alternative, same output as without.

`exiftool -g -struct -v -r /Users/emilzegers/Dropbox/Bleia/DataFit/waterschaprivierenland.nl/ > Results/waterschaprivierenland.nl-v.txt`

`exiftool -g -struct -v -r JPEG2000 > Results/JPEG2000-v.txt`

to understand structure and usage.

Then something like:

~/Downloads

```
exiftool -n -g -ext jpg -ext jpeg -ext tif -ext tiff -ext wav -ext png -ext dcf -ext webp -ext heic -ext J2C -ext J2K -ext JPC -ext JP2 -ext JPF -ext JPM -ext JPX -json JPEG2000 | jq --compact-output --arg urlBase http://mysite.net/myphotos/ '{
    "type": "FeatureCollection",
    "features": 
      map( {
        "type": "Feature", 
        "properties": {
            "date": (if (.File.FileModifyDate) then .File.FileModifyDate else "1901-01-01T00:00:00Z" end),
            "filename": .SourceFile,
            "location": {
                "address": (if (.Composite.GPSLongitude) then ("https://nominatim.openstreetmap.org/reverse?lat"+(.Composite.GPSLatitude|tostring)+"&lon="+(.Composite.GPSLongitude|tostring)+"&format=jsonv2") else "OLV Kerk, AMersfoort, Utrecht, Netherlands" end)
            },
            "raw": .,
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                if (.Composite.GPSLongitude) then .Composite.GPSLongitude else 5.3872 end,
                if (.Composite.GPSLatitude) then .Composite.GPSLatitude else 52.1552 end
            ]
        }
      } )
  }' > Results/data.json



exiftool -n -g -ext jpg -ext jpeg -ext tif -ext tiff -ext wav -ext png -ext dcf -ext webp -ext heic -ext J2C -ext J2K -ext JPC -ext JP2 -ext JPF -ext JPM -ext JPX -json -imagewidth -imageheight -composite:gpslatitude -composite:gpslongitude ~/Downloads | jq --compact-output --arg urlBase http://mysite.net/myphotos/ '{
    "type": "FeatureCollection",
    "features": 
      map( {
        "type": "Feature", 
        "properties": {"url": [$urlBase,.SourceFile] | add,
        "width": .File.ImageWidth,
        "height": .File.ImageHeight,},
        "geometry": {
          "type": "Point",
          "coordinates": [ .Composite.GPSLongitude, .Composite.GPSLatitude]}
      } )
  }' > Results/data.json
```

https://adamtheautomator.com/exiftool/

Support for over 23,000 tags over 130 different groups https://exiftool.org/#supported

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
