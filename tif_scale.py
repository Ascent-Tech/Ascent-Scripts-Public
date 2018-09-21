#!/usr/bin/python
"""
Script that can produce a bar scale for a particular length in meters to be overlaid on a geotiff.

Sometimes we crop/reduce the scale of a geotiff image and lose geographic data, so this bar scale is 
inserted beforehand in order to ensure a sense of scale is visible within the image.
"""
from PIL import Image
import sys
import numpy as np
import png

def read_tfw_file(tfw_filename):
    """
    Read data from tiff world file.
    For now, doing so manually
    @param: None
    @return: tuple of the form (dim_ns, rot, skew, dim_ew, easting, northing)
    """
    with open(tfw_filename) as f:
        dim_ns = float(f.readline())
        rot = float(f.readline())
        skew = float(f.readline())
        dim_ew = float(f.readline())
        easting = float(f.readline())
        northing = float(f.readline())
        print("Read in file with parameters:\nNorthing: {0}\tEasting: {1}\nRot: {2}\tSkew: {3}".format(northing, easting, rot, skew))
        print("Dimension NS: {0}\tDimension EW: {1}".format(dim_ns, dim_ew))
        return (dim_ns, rot, skew, dim_ew, easting, northing)

def usage():
    print("Usage: {0} <tiff file> <tfw file> [scale (m)]".format(sys.argv[0]))

def create_scale(tiff_fname, tfw_fname, scale_len=100):
    """
    Function for creating a bar scale given tiff/tfw filenames and a chosen scale length in meters.
    """
    try:
        # Acquire image info
        im = Image.open(tiff_fname)
        print("Image has structure: {0}".format(im.__str__()))

        # Acquire world info
        dim_ns, _, __, dim_ew, easting, northing = read_tfw_file(tfw_fname)

        # Check if NS and EW dimensions are equal (should be)
        assert(abs(dim_ns)==abs(dim_ew))

        # Decide line thickness
        line_width = int(np.ceil(im.height/300))

        # Infer number of pixels
        px_len = scale_len/dim_ns

        # Create PNG line of correct length
        print("Creating PNG Line of length ({0} meters/{1} pixels) to be separately overlaid on TIFF".format(scale_len, px_len))

        # Correct Image Dimension Order: Vertical, Horizontal, Colour Channel
        # Locate the 'leftmost' segments of each scale tick-mark at positions of 0.2*(line length) intervals = 0.2*(px_len+line_width)
        line_len = px_len + line_width
        line_arr = np.array([[ (0,255) for horizontal_index in range(int(line_len))] for vertical_index in range(line_width)])
        ticks_arr = np.array([[ (0,0) for horizontal_index in range(int(line_len))] for vertical_index in range(line_width)])

        # Ticks at 0.2, 0.4, 0.6, 0.8 of full horizontal length
        print("Creating ticks_arr structure")
        for vertical_index in range(line_width):
            for horizontal_index in np.round(px_len*np.arange(0.0,1.00001,0.2)).astype(int): # Use px_len here so that we can loop up to line_len = px_len + line_width
                for horizontal_offset in range(line_width):
                    ticks_arr[vertical_index][horizontal_index + horizontal_offset][1] = 255
                    #print("ticks_arr[vertical_index][horizontal_index + offset]: {0}".format(ticks_arr[vertical_index][horizontal_index+horizontal_offset]))# = (255, 255, 255, 255)

        # The last pixel in the line is at 4407, so we need to count backwards from there
        scale_arr = np.concatenate((ticks_arr, line_arr), axis=0)

        # Colour channel options and bit depth
        chan_mode = 'LA'
        bit_depth = '8'
        mode = chan_mode + ';' + bit_depth
        line_png = png.from_array(scale_arr, mode=mode)
        line_png.save(str(sys.argv[1] + ".png"))
        print("Line image written to file")
    except Exception as e:
        print("Exception: {0}".format(e))

if __name__=="__main__":
    if len(sys.argv) == 3:
        # Assume the optional scale parameter was omitted
        create_scale(sys.argv[1], sys.argv[2], 100)
    elif len(sys.argv) == 4:
        create_scale(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:
        usage()
    #main()
