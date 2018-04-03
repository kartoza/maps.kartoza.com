#!/usr/bin/python
# Script to convert NGI DEM to EPSG:3857
# Run it as python raster_projector.py -d directory-containing-tif

import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option(
    "-r", "--directory", dest="directory", help="directory to query",
    metavar="DIRECTORY")

(options, args) = parser.parse_args()

root_directory = options.directory

basedir = r'%s' % root_directory
extension = '.tif'  # do for '.tif' and '.sid'


def raster_loader():
    output_dir = 'reprojected'
    output_full_path = os.path.join('/tmp', output_dir)
    if not os.path.exists(output_full_path):
        os.mkdir(output_full_path)
    else:
        pass
    raster_output = os.path.join(output_full_path, filename)
    raster_warp = """ gdalwarp \
                -s_srs '+proj=tmerc +lat_0=0 +lon_0=%s +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' \
                -t_srs 'EPSG:3857'  -co "COMPRESS=DEFLATE" %s %s""" % (
        meridian, full_path, raster_output)
    os.system(raster_warp)


for root, dir_names, file_names in os.walk(basedir):

    for filename in file_names:
        ext = os.path.splitext(filename)[1].lower()  # extension as lowercase
        if ext == extension:
            file_base = os.path.splitext(filename)[0]  # first part of filename

            full_path = os.path.join(root, file_base) + ext  # build up path again
            central_meridian = int(filename[2:4])
            if central_meridian % 2 == 0:
                meridian = central_meridian + 1
            else:
                meridian = central_meridian

            raster_loader()
