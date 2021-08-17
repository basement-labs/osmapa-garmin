"""
OpenStreetMap boundary generator. 

Author: Andrzej Talarczyk <andrzej@talarczyk.com>

Based on work of Michał Rogalski (Rogal).

License: GPLv3.
"""
import os
import platform
import shutil


def clean(src_dir):
    """Remove target files.

    Args:
        src_dir (string): path to the directory from which target files will be removed
    """
    if os.path.isfile("{dane_osm}/poland.o5m".format(dane_osm=src_dir)):
        os.remove("{dane_osm}/poland.o5m".format(dane_osm=src_dir))
    if os.path.isfile("{dane_osm}/poland-boundaries.osm".format(dane_osm=src_dir)):
        os.remove("{dane_osm}/poland-boundaries.osm".format(dane_osm=src_dir))
    if os.path.exists("{dane_osm}/bounds".format(dane_osm=src_dir)):
        shutil.rmtree("{dane_osm}/bounds".format(dane_osm=src_dir))


def generate(bin_dir, src_dir, pbf_filename) -> int:
    """Generates boundaries. 

    Args:
        bin_dir (string): path to a directory holding compilation tools
        src_dir (string): path to a directory with source data
        pbf_filename (string): source PBF file

    Raises:
        Exception: [description]

    Returns:
        int: 0 if succes.
    """
    ret = -1

    if platform.system() == 'Windows':
        ret = os.system("start /low /b /wait {binarki}/osmconvert.exe {dane_osm}/{pbf_filename} --out-o5m >{dane_osm}/poland.o5m".format(
            binarki=bin_dir, dane_osm=src_dir, pbf_filename=pbf_filename))
        ret = os.system("start /low /b /wait {binarki}/osmfilter.exe {dane_osm}/poland.o5m --keep-nodes= --keep-ways-relations=\"boundary=administrative =postal_code postal_code=\" >{dane_osm}/poland-boundaries.osm".format(
            dane_osm=src_dir, binarki=bin_dir))
        ret = os.system("start /low /b /wait java -cp {binarki}/mkgmap.jar uk.me.parabola.mkgmap.reader.osm.boundary.BoundaryPreprocessor {dane_osm}/poland-boundaries.osm {dane_osm}/bounds".format(
            binarki=bin_dir, dane_osm=src_dir))

    elif platform.system() == 'Linux':
        ret = os.system("osmconvert {dane_osm}/{pbf_filename} --out-o5m >{dane_osm}/poland.o5m".format(
            dane_osm=src_dir, pbf_filename=pbf_filename))
        ret = os.system("osmfilter {dane_osm}/poland.o5m --keep-nodes= --keep-ways-relations=\"boundary=administrative =postal_code postal_code=\" >{dane_osm}/poland-boundaries.osm".format(
            dane_osm=src_dir))
        ret = os.system("java -cp {binarki}/mkgmap.jar uk.me.parabola.mkgmap.reader.osm.boundary.BoundaryPreprocessor {dane_osm}/poland-boundaries.osm {dane_osm}/bounds".format(
            binarki=bin_dir, dane_osm=src_dir))
            
    else:
        raise Exception("Unsupported operating system.")

    return ret