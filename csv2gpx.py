#!/usr/bin/python
"""
Convert a .csv file with northing/easting values into a Garmin waypoints file (.gpx)

author: David Fairbairn
date: September 2018

"""
import xml.etree.ElementTree as ET
import sys
import os
import csv

def xml_edit(out_tree, r_csv):
    r_out = out_tree.getroot()
    t_str = r_out.tag[:-3]
    [_, __, ___] = r_csv.next()
    elev = "690.0"
    time = "2018-09-12T12:00:00Z"
    sym = "Flag, Blue"
    for line in r_csv:
        print("Trying to add line: " + str(line))
        [label, lon, lat] = line
        elem = r_out.makeelement(t_str + 'wpt', {'lon': lon, 'lat': lat})     
        nam_e = elem.makeelement(t_str + 'name', {}) 
        nam_e.text = label
        tim_e = elem.makeelement(t_str + 'time', {})
        tim_e.text = time
        elev_e = elem.makeelement(t_str + 'ele', {})
        elev_e.text = elev
        sym_e = elem.makeelement(t_str + 'sym', {})
        sym_e.text = sym
    out_tree.write('output.GPX')
    return None

def file_edit(fname_out, r_csv):
    # Open the output file to add wpt entries to
    f_out = open(fname_out, 'rw')
    f_out.seek(-6, 2) # A proper .gpx file ends with </gpx>, which must only come AFTER our new GPS points

    elev = "690.0"
    time = "2018-09-12T12:00:00Z"
    sym = "Flag, Blue"
    [_, __, ___] = r_csv.next()
    for line in r_csv:
        print("Trying to add line: " + str(line))
        [label, lon, lat] = line
        f_out.write('<wpt lat="{0}" lon="{1}"><ele>{2}</ele><time>{3}</time><name>{4}</name><sym>{5}</sym></wpt>'.format(lat, lon, elev, time, label, sym))
    f_out.write('</gpx>')
    f_out.close()
    return 0

def usage():
    print("Usage: {0} <csv name> <example .GPX> ".format(sys.argv[0]))

if __name__=="__main__":
#    main()
    if (len(sys.argv) != 3):
        usage()
        exit()
    try:
        f_csv = open(sys.argv[1], 'r')
        r_csv = csv.reader(f_csv)
        tree = ET.parse(sys.argv[2]) 

        # Make an output tree 
        os.system('cp ./' + str(sys.argv[2]) + ' output.GPX')
        out_tree = ET.parse('output.GPX') 
        # The XML files aren't really being used for proper XML it seems

        # Call the thing 
        #main(out_tree, r_csv)
        f_out = open('output.GPX','a')
        file_edit(f_out, r_csv)
        f_out.close()
    except Exception as e:
        print("Error: {0}".format(e))
