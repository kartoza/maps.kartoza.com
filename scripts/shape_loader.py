#!/usr/bin/python
# Script to convert NGI 5m contours to EPSG:3857
# Run it as python shape_loader.py -r  /tmp/data -d kartozagis -u user -w password -p 5432 -x localhost -s schema

import fnmatch
import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option(
    "-r", "--directory", dest="directory", help="directory to query",
    metavar="DIRECTORY")
parser.add_option(
    "-d", "--database", dest="database", help="Database to be used",
    metavar="DATABASE")
parser.add_option(
    "-u", "--database-user", dest="database_user", help="Database user",
    metavar="DATABASE_USER")
parser.add_option(
    "-w", "--database-password", dest="database_password",
    help="Database password", metavar="DATABASE_PASSWORD")
parser.add_option(
    "-p", "--database-port", dest="database_port", help="Database port",
    metavar="PORT")
parser.add_option(
    "-x", "--database-host", dest="database_host", help="Database host",
    metavar="HOST")
parser.add_option(
    "-s", "--database-schema", dest="database_schema", help="Database schema",
    metavar="SCHEMA_NAME"
)

(options, args) = parser.parse_args()

root_directory = options.directory
user_name = options.database_user
user_password = options.database_password
db_port = options.database_port
db_name = options.database
db_host = options.database_host
db_schema = options.database_schema

basedir = r'%s' % root_directory
extension = '.shp'


def shp_loader(lo, table_name, db, user, password, port, host, path, schema):
    command = """ ogr2ogr -progress -append -skipfailures \
                -s_srs '+proj=tmerc +lat_0=0 +lon_0=%s +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' \
                -t_srs 'EPSG:3857'  -nln %s -nlt PROMOTE_TO_MULTI -gt 65536 -addfields \
                -lco GEOMETRY_NAME=geom -f 'PostgreSQL' \
                PG:'dbname=%s user=%s  password=%s port=%s host=%s' "%s" -lco SCHEMA=%s  """ % (
        lo, table_name, db, user, password, port, host, path, schema)
    # print 'the command is:' + command
    os.system(command)


for root, dir_names, file_names in os.walk(basedir):

    for filename in file_names:
        ext = os.path.splitext(filename)[1].lower()  # extension as lowercase
        if ext == extension:
            file_base = os.path.splitext(filename)[0]  # first part of filename

            full_path = os.path.join(root, file_base) + ext  # build up path again
            name = os.path.basename(root)
            central_meridian = int(name[2:4])
            if central_meridian % 2 == 0:
                meridian = central_meridian + 1
            else:
                meridian = central_meridian

            if fnmatch.fnmatch(filename, '*POINTS*'):
                shp_loader(central_meridian, 'hyps_elevation_points_10m', db_name, user_name, user_password, db_port,
                           db_host, full_path, db_schema)
            else:
                shp_loader(central_meridian, 'hyps_elevation_lines_10m', db_name, user_name, user_password, db_port,
                           db_host, full_path, db_schema)
