# ----------------------------------------------------------------------------------------------------------------------
# Name:        CompareCompression.py
# Py-Version:  3.x.x
# Purpose:     Takes a sample GeoTIFF and writes a table to the command line describing the
#              file size, read speed, and write speed of each GDAL compression. You can use this
#              tool to decide how to best compress a single image, or a collection of images.
#
# Notes:       The Python interpreter and GDAL must be accessible by cmd. The easiest way to do
#              this by using the python installation included with ArcGIS Pro 2.3.x and later.
#              This installation has the GDAL site package and binaries already configured. Add
#              the Python 3 interpreter to your system PATH variable to run from cmd.
#
# Credit:      Idea and code heavily borrowed from Kersten Klaus.
#              https://gist.github.com/Fernerkundung/cc3b7f77ec4534754aba
#
# Author:      Jordan Evans
#
# Created:     01/31/2019
# Last Edited: 02/06/2019(jordane)
# ----------------------------------------------------------------------------------------------------------------------

import os
import sys
import time
from hurry.filesize import size, si
import gdal
import pandas

# ----------------------------------------------------------------------------------------------------------------------
# Set source image GeoTIFF
src_img = os.path.abspath(sys.argv[1])

# Create a temporary directory
tmp_dir = os.path.join(os.path.dirname(src_img), "tmp")
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# Set the file path variables for the output paths
uncompressed = os.path.join(tmp_dir, 'uncompressed.tif')
packbits = os.path.join(tmp_dir, 'packbits.tif')
deflate_1 = os.path.join(tmp_dir, 'deflate_1.tif')
deflate_2 = os.path.join(tmp_dir, 'deflate_2.tif')
lzw_1 = os.path.join(tmp_dir, 'lzw_1.tif')
lzw_2 = os.path.join(tmp_dir, 'lzw_2.tif')

# List of path variables
files = [uncompressed, packbits, deflate_1, deflate_2, lzw_1, lzw_2]

# List of Columns and Rows for the pandas output table
columns = ["Uncompressed", "Packbits", "Deflate pred=1",
           "Deflate pred=2", "LZW pred=1", "LZW pred=2"]
rows = ["Size", "Write time", "Read time"]


# ----------------------------------------------------------------------------------------------------------------------
def generate_compressed_images(in_files, input_image):
    """
    Converts the input file to every kind of GDAL compression and saves the time
    it takes to write each file.
    """
    try:
        print('|BEGIN - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        # Set Command variables for GDAL_Translate
        command_uncompressed = "-of GTiff -co \"BIGTIFF=IF_SAFE\""
        command_packbits = "-of GTiff -co \"BIGTIFF=IF_SAFE\" -co \"COMPRESS=PACKBITS\" -co \"TILED=YES\""
        command_deflate_1 = "-of GTiff -co \"BIGTIFF=IF_SAFE\" -co \"COMPRESS=DEFLATE\" -co \"PREDICTOR=1\" -co \"TILED=YES\""
        command_deflate_2 = "-of GTiff -co \"BIGTIFF=IF_SAFE\" -co \"COMPRESS=DEFLATE\" -co \"PREDICTOR=2\" -co \"TILED=YES\""
        command_lzw_1 = "-of GTiff -co \"BIGTIFF=IF_SAFE\" -co \"COMPRESS=LZW\" -co \"PREDICTOR=1\" -co \"TILED=YES\""
        command_lzw_2 = "-of GTiff -co \"BIGTIFF=IF_SAFE\" -co \"COMPRESS=LZW\" -co \"PREDICTOR=2\" -co \"TILED=YES\""

        # Declare write speed variables
        write_uncompressed = ''
        write_packbits = ''
        write_deflate_1 = ''
        write_deflate_2 = ''
        write_lzw_1 = ''
        write_lzw_2 = ''

        # set gdal values
        for file in in_files:
            start_time = time.time()
            dest_name = file
            src_ds = input_image
            if file == uncompressed:
                gdal.Open(src_ds)
                translate_options = gdal.TranslateOptions(
                    gdal.ParseCommandLine(command_uncompressed))
                gdal.Translate(dest_name, src_ds, options=translate_options)
                write_uncompressed = time.time() - start_time
                continue

            elif file == packbits:
                gdal.Open(src_ds)
                translate_options = gdal.TranslateOptions(
                    gdal.ParseCommandLine(command_packbits))
                gdal.Translate(dest_name, src_ds, options=translate_options)
                write_packbits = time.time() - start_time
                continue

            elif file == deflate_1:
                gdal.Open(src_ds)
                translate_options = gdal.TranslateOptions(
                    gdal.ParseCommandLine(command_deflate_1))
                gdal.Translate(dest_name, src_ds, options=translate_options)
                write_deflate_1 = time.time() - start_time
                continue

            elif file == deflate_2:
                gdal.Open(src_ds)
                translate_options = gdal.TranslateOptions(
                    gdal.ParseCommandLine(command_deflate_2))
                gdal.Translate(dest_name, src_ds, options=translate_options)
                write_deflate_2 = time.time() - start_time
                continue

            elif file == lzw_1:
                gdal.Open(src_ds)
                translate_options = gdal.TranslateOptions(
                    gdal.ParseCommandLine(command_lzw_1))
                gdal.Translate(dest_name, src_ds, options=translate_options)
                write_lzw_1 = time.time() - start_time
                continue

            elif file == lzw_2:
                gdal.Open(src_ds)
                translate_options = gdal.TranslateOptions(
                    gdal.ParseCommandLine(command_lzw_2))
                gdal.Translate(dest_name, src_ds, options=translate_options)
                write_lzw_2 = time.time() - start_time
                continue

            else:
                continue

        output_write_speeds = [write_uncompressed, write_packbits,
                               write_deflate_1, write_deflate_2, write_lzw_1, write_lzw_2]

        # Console Success...
        print('|SUCCESS - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        return output_write_speeds

    # Handles errors in general and 'err' holds the details of the error collected...
    except Exception as err:
        print('|FAIL - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + ' - ' + str(err) + '|\n')


# ----------------------------------------------------------------------------------------------------------------------
def calculate_file_size(in_files):
    """
    Calculates the size of each output GeoTIFF
    """
    try:
        print('|BEGIN - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        # Define file size variables
        size_uncompressed = ''
        size_packbits = ''
        size_deflate_1 = ''
        size_deflate_2 = ''
        size_lzw_1 = ''
        size_lzw_2 = ''

        for file in in_files:
            if file == uncompressed:
                size_uncompressed = size(os.path.getsize(file), system=si)
                continue

            elif file == packbits:
                size_packbits = size(os.path.getsize(file), system=si)
                continue

            elif file == deflate_1:
                size_deflate_1 = size(os.path.getsize(file), system=si)
                continue

            elif file == deflate_2:
                size_deflate_2 = size(os.path.getsize(file), system=si)
                continue

            elif file == lzw_1:
                size_lzw_1 = size(os.path.getsize(file), system=si)
                continue

            elif file == lzw_2:
                size_lzw_2 = size(os.path.getsize(file), system=si)
                continue

            else:
                continue

        output_file_sizes = [size_uncompressed, size_packbits,
                             size_deflate_1, size_deflate_2, size_lzw_1, size_lzw_2]

        # Console Success...
        print('|SUCCESS - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        return output_file_sizes

    # Handles errors in general and 'err' holds the details of the error collected...
    except Exception as err:
        print('|FAIL - ' + os.path.basename(os.path.realpath(__file__)) + ' @ ' + sys._getframe().f_code.co_name + ' - '
              + str(err) + '|\n')


# ----------------------------------------------------------------------------------------------------------------------
def calculate_read_times(in_files):
    """
    Calculates how long it takes to read each file
    """

    try:
        print('|BEGIN - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        # Declare read speed variables
        read_uncompressed = ''
        read_packbits = ''
        read_deflate_1 = ''
        read_deflate_2 = ''
        read_lzw_1 = ''
        read_lzw_2 = ''

        def read_tif(tif):
            return gdal.Open(tif).ReadAsArray()

        for file in in_files:
            if file == uncompressed:
                start_time = time.time()
                read_tif(file)
                read_uncompressed = time.time() - start_time
                continue

            elif file == packbits:
                start_time = time.time()
                read_tif(file)
                read_packbits = time.time() - start_time
                continue

            elif file == deflate_1:
                start_time = time.time()
                read_tif(file)
                read_deflate_1 = time.time() - start_time
                continue

            elif file == deflate_2:
                start_time = time.time()
                read_tif(file)
                read_deflate_2 = time.time() - start_time
                continue

            elif file == lzw_1:
                start_time = time.time()
                read_tif(file)
                read_lzw_1 = time.time() - start_time
                continue

            elif file == lzw_2:
                start_time = time.time()
                read_tif(file)
                read_lzw_2 = time.time() - start_time
                continue

            else:
                continue

        output_read_speeds = [read_uncompressed, read_packbits,
                              read_deflate_1, read_deflate_2, read_lzw_1, read_lzw_2]

        # Console Success...
        print('|SUCCESS - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        return output_read_speeds

    # Handles errors in general and 'err' holds the details of the error collected...
    except Exception as err:
        print('|FAIL - ' + os.path.basename(os.path.realpath(__file__)) + ' @ ' + sys._getframe().f_code.co_name + ' - '
              + str(err) + '|\n')


# ----------------------------------------------------------------------------------------------------------------------
def remove_directory(in_files, delete_directory):
    """
    Prints results to a table that is displayed in the command line.
    """

    try:
        print('|BEGIN - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        for file in in_files:
            os.remove(file)
        os.removedirs(delete_directory)

        # Console Success...
        print('|SUCCESS - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

    # Handles errors in general and 'err' holds the details of the error collected...
    except Exception as err:
        print('|FAIL - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + ' - ' + str(err) + '|\n')


# ----------------------------------------------------------------------------------------------------------------------
def print_results(in_sizes, in_writes, in_reads, in_rows, in_columns):
    """
    Prints results to a table that is displayed in the command line.
    """

    try:
        print('|BEGIN - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        print(pandas.DataFrame(
            [in_sizes, in_writes, in_reads], in_rows, in_columns))

        # Console Success...
        print('|SUCCESS - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

    # Handles errors in general and 'err' holds the details of the error collected...
    except Exception as err:
        print('|FAIL - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + ' - ' + str(err) + '|\n')


# ----------------------------------------------------------------------------------------------------------------------
def main():

    try:
        # Log Runtime...
        start = time.time()

        # Console Begin...
        print('|BEGIN - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        # Area Status function...
        writes = generate_compressed_images(files, src_img)
        sizes = calculate_file_size(files)
        reads = calculate_read_times(files)
        remove_directory(files, tmp_dir)
        print_results(sizes, writes, reads, rows, columns)

        # Console Success...
        print('|SUCCESS - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + '|\n')

        # Log Runtime
        end = time.time()
        total_time = end - start
        print('Run Time = ' + str(total_time) + ' seconds')

    # Handles errors in general and 'err' holds the details of the error collected...
    except Exception as err:
        print('|FAIL - ' + os.path.basename(os.path.realpath(__file__)) +
              ' @ ' + sys._getframe().f_code.co_name + ' - ' + str(err) + '|\n')


# ----------------------------------------------------------------------------------------------------------------------
# Call main function if condition met...
if __name__ == '__main__':
    main()
