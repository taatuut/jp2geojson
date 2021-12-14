# jp2geojson

Converting JPEG 2000 / JP2 metadata to geojson using Python.

Redub to "jolly pictures to geojson" after finding `exiftool` that does a lot of the needed stuff...

(Why is it that you always find somehting useful after starting creating it yourself? Sort of rubberducking but different...)

# Inspiration

https://exiftool.org/

https://github.com/Visgean/photos2geojson

https://stackoverflow.com/questions/17858404/creating-a-tree-deeply-nested-dict-from-an-indented-text-file-in-python

https://gist.github.com/cquest/777faa6268d848f0a6e2

NOTE: Also tried using `pyyaml` for this purpose but the text output is not wellformed enough for that.

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


--arg urlbase http://mysite.net/myphotos/ 
~/downloads


```
exiftool -n -g -ext jpg -ext jpeg -ext jpe -ext tif -ext gif -ext bmp -ext exe -ext doc -ext docx -ext xls -ext xlsx -ext ppt -ext pptx -ext odf -ext pdf -ext bmp -ext tiff -ext wav -ext png -ext dcf -ext webp -ext heic -ext heif -ext hif -ext html -ext htm -ext xhtml -ext j2c -ext j2k -ext jpc -ext jp2 -ext jpf -ext jpm -ext jpx -json -r ~/downloads | jq --compact-output '{
    "type": "FeatureCollection",
    "features": 
      map( {
        "type": "Feature", 
        "properties": {
            "date": (if (.File.FileModifyDate) then .File.FileModifyDate else "1901-01-01T00:00:00Z" end),
            "filename": .SourceFile,
            "location": {
                "address": (if (.Composite.GPSLongitude) then ("https://nominatim.openstreetmap.org/reverse?lat="+(.Composite.GPSLatitude|tostring)+"&lon="+(.Composite.GPSLongitude|tostring)+"&format=jsonv2") else "OLV Kerk, Amersfoort, Utrecht, Netherlands" end)
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
```

https://adamtheautomator.com/exiftool/

Support for over 23,000 tags over 130 different groups https://exiftool.org/#supported

# Not exiftool...

First try was DIY with Python... nice exercise, but `exiftool` does it better :-)

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

E.g:

```
<ns4:GPSLatitude>42,20.56N</ns4:GPSLatitude>
<ns4:GPSLongitude>71,5.29W</ns4:GPSLongitude>
<ns4:GPSTimeStamp>2013-02-09T19:47:53Z</ns4:GPSTimeStamp>
<ns4:GPSMapDatum>WGS-84</ns4:GPSMapDatum>
```

NOTE: not yet doing anything with `GPSMapDatum` and other GPS tags.

NOTE: a result map html file based on `leaflet.html` template can be created. It does show the markers but not the images as these cannot be previewed in the browser (?). Some code tp create default markers for images without GPS info, needs some more work.

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
