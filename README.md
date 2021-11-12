# HLS-Live-Traffic-Generator

This is a small utility that enables one to simulate typical network traffic when end users are viewing HTTP Live Streaming (HLS).

When setting up and configuring corporate traffic shaping (QoS), corporate VPN setting, this tool can come in handy for IT teams to test their setting by simulating a fare amount of typical live video streaming network traffic.


## Running the tool
The tool is a simple interactive command line program written in Python.

To run the tool, launch it with the following parameters:

```
python3 HLS_live_traffic_generator.py [m3u8_url] [download_folder] [nb_segments_to_download] [nb_of_threads] [variant_number]

```
Example:

```
python3 HLS_live_traffic_generator.py https://[your_cdn_domain]/index.m3u8 test/ 30 10 1
```

In the above example command line:

```
test/ = the folder in which the segments and playlists will be downloaded to (create the folder prior launching the script)
30 = the number of video segments to download in that test
10 = the number of downloader threads (one thread = one user)
1 = the variant playlist to download (highest resolution = highest possible load on the network)

```
