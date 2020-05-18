# gpx2avi
Converts GPX track to AVI mediafile with visualization of your tracks  
  
## gps2avi_osm_static.py
Uses OpenStreetMap to get map data.  
Script utilizes [StaticMap API](https://wiki.openstreetmap.org/wiki/Static_map_images) and Python implementation of [StaticMapShellScript](https://wiki.openstreetmap.org/wiki/StaticMapShellScript)  

### Dependencies
1. Python3  
2. [gpxpy](https://pypi.org/project/gpxpy/)  
3. [Flask](https://flask.palletsprojects.com/)  
4. Firefox  
5. ffmpeg

All required dependencies can be installed this way:  
```bash
sudo apt install python3 firefox ffmpeg
pip3 install gpxpy flask
```
  
### Usage
1. Start sleep server (_sleep.py_ script). Firefox in headless takse a screenshot of the page before it has made the AJAX request, so this is helper script to provide 5 seconds delay before taking screenshot.  
2. Run _gps2avi\_osm\_static.py_ script. Result file will be named YOUR_TRACK.gpx.mp4  
```bash
FLASK_APP=sleep.py flask run
gps2avi_osm_static.py YOUR_TRACK.gpx
```