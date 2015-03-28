VITCloud
========

VITCloud is a file indexing service for the VIT hostels to help people discover what others have already downloaded and getting it from them instead of redownloading.

The users only have install a client app, and it scans and sends the index to the central server, which can be viewed online by other students.


### Currently Accepted API Format: 

* Filename, size (in bytes)

```
{
  "Room": "447",
  "Hostel": "Boys",
  "Block": "E",
  "Files": [
    "Auto\u0301mata.2014.720p.BluRay.x264.YIFY.mp4",
    "854742180",
    "The.Equalizer.2014.720p.BluRay.x264.YIFY.mp4",
    "915886549",
    "The.Maze.Runner.2014.720p.BluRay.x264.YIFY.mp4",
    "853995484",
    "The.Congress.2013.720p.BluRay.900MB.ShAaNiG.mkv",
    "943787501",
    "The.Newsroom.2012.S03E05.HDTV.x264-KILLERS.mp4",
    "382772000",
    "Windows 7 Ultimate SP1 (64 Bit).iso",
    "3182010368",
  ]
}
```



Client Apps:
===

- Mac: [VITCloud-Client-Mac] 
- Windows: [VITcloud-Client-Windows](https://github.com/aneesh-neelam/VITcloud-Client-Windows)
- Linux: In Developement


[VITCloud-Client-Mac]:https://github.com/biocross/VITCloud-Client-Mac
