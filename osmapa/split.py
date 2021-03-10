"""OpenStreetMap splitter.

Author: Andrzej Talarczyk <andrzej@talarczyk.com>

Based on work of Michał Rogalski (Rogal).

License: GPLv3.
"""
import os
import platform
import shutil

def do(bin_dir, data_dir, pbf_filename, dest_dir, map_id):
    """Do the actual splitting of the source map.

    Args:
        bin_dir (string): path to a directory holding compilation tools
        data_dir (string): path to a directory with source data
        pbf_filename (string): source PBF file
        dest_dir (string): directory to hold a splitted map
        map_id (string): map ID
    """

    # Check if the directory to hold splitted map exists, if not - create it.
    if (not os.path.isdir(dest_dir)):
         os.mkdir(dest_dir)

    # Go to the directory to hold a splitted map.
    os.chdir(dest_dir)

    # Try to remove contents of the directory to hold a splitted map.
    try:
        for f in os.listdir("."):
            os.remove(f)
    except:
        pass

    # Do the splitting.
    ret = -1
    if platform.system() == 'Windows':
        ret = os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {bin_dir}/splitter.jar --keep-complete=true --mapid={map_id} --max-nodes=1600000 {data_dir}/{pbf_filename}'.format(
        map_id=map_id, data_dir=data_dir, bin_dir=bin_dir, pbf_filename=pbf_filename))
    elif platform.system() == 'Linux':
        ret = os.system('java -enableassertions -Xmx6000m -jar {bin_dir}/splitter.jar --keep-complete=true --mapid={map_id} --max-nodes=1600000 {data_dir}/{pbf_filename}'.format(
        data_dir=data_dir, map_id=map_id, bin_dir=bin_dir, pbf_filename=pbf_filename))
    else:
        raise Exception("Unsupported operating system.")

    if(ret == 0):
        print("The map has been split.")
    else:
        raise Exception("Blad splitowania danych OSM")

def clean(mapa_root, split_dir):
    """Clean up a directory to hold split map.

    Args:
        dest_dir (string): the directory to be cleaned up
    """
    os.chdir(mapa_root)
    shutil.rmtree(split_dir, True)


if __name__ == "__main__":
    import sys
    primary_def_name = "osmapa.split.do()"
    if (len(sys.argv) < 6):
        print("You are trying to run {primary_def_name} as script but not all required parameters have been given. Stop.".format(primary_def_name=primary_def_name))
    else:
        print("Running {primary_def_name} as script...".format(primary_def_name=primary_def_name))
        do(bin_dir=sys.argv[1], data_dir=sys.argv[2], pbf_filename=sys.argv[3], dest_dir=sys.argv[4], map_id=sys.argv[5])
        print("Split {pbf_filename} to {dest_dir} for map {map_id}.".format(pbf_filename=sys.argv[3], dest_dir=sys.argv[4], map_id=sys.argv[5]))