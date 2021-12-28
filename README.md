# jp2geojson

Converting JPEG 2000 metadata to geojson using Python, uh make that exiftool, and maybe use a Python wrapper later on<sup>*</sup>. Taking inspiration from https://github.com/Visgean/photos2geojson

Redub to "jolly philes to geojson" after finding `exiftool` that does a lot of the needed stuff and way more. So actually going to extract data from more file types than JPEG 2000 only. Chapeau Phil Harvey! https://github.com/exiftool/exiftool

<sup>*</sup>) Why is it that you always find somehting more useful after starting creating it yourself? Sort of rubberducking but different...

NOTE: creating this to use in DataEther Data Fitness solution so setup is configured to work well with MongoDB Atlas, the data platform for Data Fitness, and part of the processing (like the rounding of coordinates, and making sure every document has custom or default coordinates to ease 2dshpere index creation) is aimed at further processing and analysing the results in Data Fitness. The general setup of metadata extraction mimics 

# exiftool

Assumes `exiftool`, `jq` installed and available in path

Open terminal in folder `jp2geojson`

First tests:

```
exiftool JPEG2000/ > Results/data.txt
exiftool -json JPEG2000/ > Results/data.json
exiftool -json -g -struct -r path/to/folder/with/subfolders > Results/folder_with_subfolders.nl.json
exiftool -json -g -struct -r JPEG2000 > Results/JPEG2000.json
```

Prefer `-g` over `-G4`.

For verbose output, add `-v` Output size goes from 569 kb (json) to 45 Mb (txt). Also quite CPU intensive.

NOTE: cannot combine verbose with json output as using verbose ignores most other options, see https://exiftool.org/exiftool_pod.html Using -v0 is not an alternative, same output as without.

Look at results from below command to understand structure and usage.

`exiftool -g -struct -v -r JPEG2000 > Results/JPEG2000-v.txt`

`exiftool -g -struct -v -r path/to/folder/with/subfolders > Results/folder_with_subfolders-v.txt`

Some more exploration:

Can use `--arg urlbase http://mysite.net/myphotos/` with `jq` but args not needed here now.

Exiftool extracts lots of useful information from other files than imagery too.

Store complete exiftool result in `raw` in resulting geojson. TODO: trim down to use only selected Group Names from Family 0 (Information Type),

Extensions to process:

```
-ext avi -ext bmp -ext dcf -ext dib -ext dll -ext doc -ext docx -ext dylib -ext exe -ext flv -ext gif -ext heic -ext heif -ext hif -ext ical -ext ics -ext iso -ext j2c -ext j2k -ext jp2 -ext jpc -ext jpe -ext jpeg -ext jpf -ext jpg -ext jpm -ext jpx -ext lif -ext lnk -ext m2v -ext mov -ext mp3 -ext mp4 -ext mpeg -ext mpg -ext numbers -ext odf -ext pdf -ext pdsd -ext png -ext pps -ext ppsx -ext ppt -ext pptx -ext psb -ext psp -ext qt -ext raw -ext rif -ext riff -ext rtf -ext svg -ext swf -ext tif -ext tiff -ext vcard -ext vcf -ext wav -ext webm -ext webp -ext wma -ext wmv -ext xls -ext xlsx
```

NOTE: The biggest problem with Perl is its lack of support for Windows Unicode file names. https://exiftool.org/under.html

All files, no print conversion. Can use `-c "%.4f degrees"` with four decimals for sufficient accuracy (more deciamls is 'false promise' for GPS generated data). Option `-c` does not go well with `-p`, use `jq` to process coordinates etc.

TIP: `history | cut -c 8-` History wothout line numbers

TODO:

Use regex to remove special characters `/[\r\n\x0B\x0C\u0085\u2028\u2029]+/g` ?

Run another test using `-X (-xmlFormat)` instead of json output. Use RDF/XML output format could be interesting input for Triply?

For now concentrating on the following file types in descending priority order:

Media

- image
- multimedia

Office

- office
- pdf

System

- diskimage
- executable
- shortcut

```
exiftool -fast2 -q -q -n -g -ext avi -ext bmp -ext dcf -ext dib -ext dll -ext doc -ext docx -ext dylib -ext exe -ext flv -ext gif -ext heic -ext heif -ext hif -ext ical -ext ics -ext iso -ext j2c -ext j2k -ext jp2 -ext jpc -ext jpe -ext jpeg -ext jpf -ext jpg -ext jpm -ext jpx -ext lif -ext lnk -ext m2v -ext mov -ext mp3 -ext mp4 -ext mpeg -ext mpg -ext numbers -ext odf -ext pdf -ext pdsd -ext png -ext pps -ext ppsx -ext ppt -ext pptx -ext psb -ext psp -ext qt -ext raw -ext rif -ext riff -ext rtf -ext svg -ext swf -ext tif -ext tiff -ext vcard -ext vcf -ext wav -ext webm -ext webp -ext wma -ext wmv -ext xls -ext xlsx -json -efile7! path/to/output/data_error.txt -r "path/to/folder/to/scan" | jq --compact-output '{
"type": "FeatureCollection",
"features":
    map( {
    "type": "Feature",
    "properties": {
        "date": (if (.File.FileModifyDate) then .File.FileModifyDate else "1901-01-01T00:00:00Z" end),
        "filename": .SourceFile,
        "location": {
            "address": (if (.Composite.GPSLongitude and .Composite.GPSLongitude != "") then ("https://nominatim.openstreetmap.org/reverse?lat="+(.Composite.GPSLatitude|tostring)+"&lon="+(.Composite.GPSLongitude|tostring)+"&format=jsonv2") elif (.EXIF.GPSLongitude and .EXIF.GPSLongitude != "") then ("https://nominatim.openstreetmap.org/reverse?lat="+(.EXIF.GPSLatitude|tostring)+"&lon="+(.EXIF.GPSLongitude|tostring)+"&format=jsonv2") elif (.XMP.GPSLongitude and .XMP.GPSLongitude != "") then ("https://nominatim.openstreetmap.org/reverse?lat="+(.XMP.GPSLatitude|tostring)+"&lon="+(.XMP.GPSLongitude|tostring)+"&format=jsonv2") else "OLV Kerk, Amersfoort, Utrecht, Netherlands" end)
        },
        "raw": .,
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            if (.Composite.GPSLongitude and .Composite.GPSLongitude != "") then .Composite.GPSLongitude elif (.EXIF.GPSLongitude and .EXIF.GPSLongitude != "") then .EXIF.GPSLongitude elif (.XMP.GPSLongitude and .XMP.GPSLongitude != "") then .XMP.GPSLongitude else 5.3872 end,
            if (.Composite.GPSLatitude and .Composite.GPSLatitude != "") then .Composite.GPSLatitude elif (.EXIF.GPSLatitude and .EXIF.GPSLatitude != "") then .EXIF.GPSLatitude elif (.XMP.GPSLatitude and .XMP.GPSLatitude != "") then .XMP.GPSLatitude else 52.1552 end
        ]
    }
    } )
}' >  path/to/output/data.json
```

Results in `data.json` with geojson results, and `data_error.txt` with error information.

NOTE: direct piping of `exiftool` to `jq` with above setup keeps everything in memory until complete scan is done. If memory is not sufficient for that, make it a two step approach: write to `.json` with `exiftool` and pickup that file with `jq` for furtehr processing. 
Run on `data.json` containing the `FeatureCollection`:

`jq --compact-output '.features' jqpath/to/output/data.json > path/to/output/features.json`

Run command on `features.json` containing the array with features `[{"type":"Feature", ...},{"type":"Feature", ...},{"type":"Feature", ...}]`:

`jq --compact-output '.[] | if (.properties.location.address != "OLV Kerk, Amersfoort, Utrecht, Netherlands") then (.geometry.coordinates[0] = (.geometry.coordinates[0] * 10000 | floor / 10000) | .geometry.coordinates[1] = (.geometry.coordinates[1] * 10000 | floor / 10000)) | .properties += {"gps": "True"} else . | .properties += {"gps": "False"} end' path/to/output/features.json > path/to/output/rounded_features.json`

Gives output in `rounded_features.json` as a new line separated sequence, so don't use `--array` with `mongoimport`. Could look at storing back in an array (would then be one line, bit more compact).

TIP: handy regex pattern to find something that does not look like the regular... `/geometry":[^{]/gm`. In `VS Code` or `Notepad++` don't the `/../gm`. Use https://regex101.com/ for testing regexes.

# General

Some issues with quotes when transferring command from MacOS to Window. Use Git bash from Git for Windows Portable at https://git-scm.com/download/win 

Test generated geojson online with http://geojson.io/

Use the following code to generate a requirements.txt file:

```
python3 -m pip install pipreqs
cd /path/to/jp2geojson
pipreqs . --force
```

More on pipreqs at https://github.com/bndr/pipreqs

NOTE: don't use `pip freeze` for this purpose, because it saves all packages in the environment including those not needed in the current project)

TIP: a simple but cool `curl` and `jq` test: `curl http://api.open-notify.org/iss-now.json | jq '.'` (source: https://www.baeldung.com/linux/jq-command-json)

```
for i in *.json; do wc -l "$i"; done
wc -l *.json
find //wsl-fs01.wsl.lan/4_Programma_watersysteem_en_keten/ -type f -printf '.' | wc -c
find //wsl-fs01.wsl.lan/4_Programma_watersysteem_en_keten/ -type d -printf '.' | wc -c
```

# Inspiration

https://exiftool.org/

https://exiftool.org/exiftool_pod.html

Support for over 23,000 tags over 130 different groups https://exiftool.org/#supported

https://adamtheautomator.com/exiftool/

https://github.com/Visgean/photos2geojson

https://stackoverflow.com/questions/17858404/creating-a-tree-deeply-nested-dict-from-an-indented-text-file-in-python

https://gist.github.com/cquest/777faa6268d848f0a6e2

https://webgeodatavore.com/jq-json-manipulation-command-line-with-geojson.html

https://gist.github.com/arbakker/dd339a92f83a68c78136573d7ae08147

NOTE: Also tried using `pyyaml` for this purpose but the text output is not wellformed enough for that.

# Pre-exiftool...

First try was DIY with Python... See `main.py`. Nice exercise, but `exiftool` does it better :-) Disabandoned now and everything below is only left in this README for "historical reasons" (if history cares).

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
