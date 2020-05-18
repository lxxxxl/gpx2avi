#!/usr/bin/env python3
import os
import os.path
import sys
import shutil
import urllib.request
import subprocess
import time
import base64
import gpxpy

if len(sys.argv) != 2:
    print('Usage: {0} PATH_TO_TRACKFILE.gpx'.format(__file__))
    exit(0)

gpx_filename = sys.argv[1]
tempdir = '{}_tmp'.format(gpx_filename)

zoom = 20
sleep_script_url = 'http://127.0.0.1:5000/sleep/5'

# remove old files and create temporary directory to store video frames
if os.path.exists(tempdir):
    shutil.rmtree(tempdir, ignore_errors=True)
os.mkdir(tempdir)
if os.path.isfile(gpx_filename+'.mp4'):
    os.unlink(gpx_filename+'.mp4')

# open track file for reading
gpx_file = open(gpx_filename, 'r')
gpx = gpxpy.parse(gpx_file)

counter = 0
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.time))

            # this is python implementation of StaticMapShellScript.
            # More info can be found here: https://wiki.openstreetmap.org/wiki/StaticMapShellScript

            # ompute the correct URL for the slippymap.
            scale = round(360 * (0.5**zoom),6)
            left   = point.longitude - scale
            right  = point.longitude + scale
            top    = point.latitude - scale
            bottom = point.latitude + scale
            
            url='https://www.openstreetmap.org/export/embed.html?bbox={0},{1},{2},{3}&layer=mapnik&marker={4},{5}'\
                .format(left, top, right, bottom, point.latitude, point.longitude)
            
            # Generate the webpage, and convert to a data-url. 
            # Note that sleep is a trivial script that sleeps for N seconds before responding. It means that the main iframe's JS has
            # time to complete, before firefox thinks that the page is "ready" and screenshots it.
            page = '<html><body>' \
                '<iframe style="width:100vw; height:100vh" frameborder=0 scrolling=no marginheight=0 marginwidth=0 src="{0}"></iframe>' \
                '<iframe src="{1}" style="display:none" width=1 height=1></iframe>' \
                '</body></html>' \
                    .format(url, sleep_script_url)
            data = 'data:text/html;base64,' + base64.b64encode(page.encode('ascii')).decode('ascii')	#Make this "micro webpage" a data-url.

            # Now call Firefox in headless mode to take screenshot
            frame_filename = '{0}/{1:05}.png'.format(tempdir, counter)
            subprocess.call('firefox --headless --window-size 1600,1200 --screenshot "{0}" "{1}"'.format(frame_filename, data), shell=True)

            counter += 1

# Concat all frames into slideshow
subprocess.call('ffmpeg -framerate 1 -i "{0}_tmp/%05d.png" -c:v libx264 -vf fps=15 -pix_fmt yuv420p "{0}.mp4"'.format(gpx_filename), shell=True)
