 E:/exiftool-12.37/exiftool.exe -n -g -json -r //wsl-fs01.wsl.lan/4_Programma_watersysteem_en_keten/11_Ecologie | E:/jq/jq-win64.exe --compact-output '{
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
  }' >  E:/datafitness/controloneagent/Logs/Geojson/data_allfiles.json

Need better check for lat/lon to always get valid numeric info otherwise 2dsphere index will fail (useful test)

To enable long path names on Windows 10 change registry key:

`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`

`LongPathsEnabled`

Had to start a cmd with Run as Administrator first, then start regedit there then make edit.

https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation

https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/

Is this setting now also available in new Git bash session? Test...

Issue still happens

Otherwise use cmd with Run as Administrator, and solve queting issue...