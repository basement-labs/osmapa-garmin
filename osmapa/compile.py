"""OpenStreetMap Garmin map compiler.

Author: Andrzej Talarczyk <andrzej@talarczyk.com>

Based on work of Michał Rogalski (Rogal).

License: GPLv3.
"""
import os
import platform
import shutil

def prepare(dest_dir, split_source_dir):
    """Prepare a working directory for map compilation.

    Args:
        dest_dir (string):  working directory for map compilation
        split_source_dir (string): directory containing a split map
    """

    try:
        print("Usuwanie zawartosci katalogu: " + dest_dir)
        shutil.rmtree(dest_dir, True)

    except Exception:
        pass

    os.mkdir(dest_dir)

    print("Kopiowanie danych zrodlowych (split) do folderu " + dest_dir)

    if(len(os.listdir(split_source_dir)) == 0):
        raise Exception("Katalog {source} jest niedostepny lub pusty!".format(
            split_source_dir=split_source_dir))

    for plik in os.listdir(split_source_dir):
        shutil.copy(split_source_dir + "/" + plik, dest_dir)


def produce(bin_dir, mapa_root, map_work_dir, typfile, style, configfile, fid, src_dir, map_version, publisher_id, map_name, out_dir, coastlinefile="", bounds_subdir="", lowercase=False, codepage="", verbose=False):
    """Compile a distrubution set for a single map.

    Args:
        bin_dir (string): path to a directory holding compilation tools
        mapa_root (string): path to the root directory of a map production environment
        map_work_dir (string): path to a map compilation working directory
        typfile (string): name of a .typ file to be used
        style (string):  name of the style to be used 
        configfile (string): name of the mkgmap configuration file to be used
        fid (string): map identifier
        src_dir (string): path to a directory with source data
        map_version (string): string with map version
        publisher_id (string): publisher ID to be used (2-digit)
        map_name (string): alphanumeric map name to be used
        out_dir (string): path to a directory where the produced map distribution set will be placed
        coastlinefile (string): name of a PBF file containing coastlines (optional)
        bounds_subdir (string): name of a subdirectory relative to src_dir where bouds data is located
        lowercase (boolean): whether to include --lower-case parameter in mkgmap call
        codepage (string): Windows code page ID (e.g. "1250" for Polish)
        verbose (boolean): whether to include --verbose parameter in mkgmap call

    Returns:
        None
    """

    # Process optional parameters.
    param_coastline = "" if coastlinefile == "" else '--coastlinefile={src_dir}/{coastlinefile}'.format(src_dir=src_dir, coastlinefile=coastlinefile)
    param_bounds = "" if bounds_subdir == "" else '--bounds={src_dir}/{bounds_subdir}'.format(src_dir=src_dir, bounds_subdir=bounds_subdir)
    param_lowercase = '--lower-case' if lowercase else ""
    param_codepage = "" if codepage == "" else '--code-page={codepage}'.format(codepage=codepage)
    param_verbose = "--verbose" if verbose else ""


    os.chdir(map_work_dir)

    if (typfile != None and len(typfile) > 0):
        tmp_typ_filename = "style.typ"
        shutil.copy(bin_dir + "/typ/" + typfile, tmp_typ_filename)
    else: 
        tmp_typ_filename = ""
    
    ret = -1
    command = 'java -enableassertions -Xmx6000m -jar {bin_dir}/mkgmap/mkgmap.jar {param_verbose} --family-name={map_name} --description={map_name} --series-name={map_name}  {param_coastline}  --read-config={mapa_root}/config/{configfile} {param_bounds} --family-id={fid} --product-id={fid} --mapname={publisher_id}{fid}001 --overview-mapname={publisher_id}{fid}000   --style-file={bin_dir}/resources/styles/ --style={styl}  --check-styles {param_lowercase} {param_codepage} -c template.args  {tmp_typ_filename}'.format(
            mapa_root=mapa_root, bin_dir=bin_dir, styl=style, configfile=configfile, fid=fid, publisher_id=publisher_id,map_name=map_name, src_dir=src_dir, tmp_typ_filename=tmp_typ_filename, param_verbose=param_verbose, param_lowercase=param_lowercase, param_codepage=param_codepage, param_coastline=param_coastline, param_bounds=param_bounds)

    if platform.system() == 'Windows':
        command = 'start /low /b /wait ' + command

    print("Command: {command}".format(command=command))
    if platform.system() == 'Windows' or platform.system() == 'Linux':
        ret = os.system(command)
    else:
        raise Exception("Unsupported operating system.")

    print("kompiluj_mape - mkgmap return value: " + str(ret))

    # mkgmap has created an NSI file named as follows.
    nsi_filename = "{publisher_id}{fid}000.nsi".format(publisher_id=publisher_id, fid=fid)

    # When compiling 66004000.nsi file on Linux, a directive "Unicode True" must be added on top of it.
    if not os.path.isfile(nsi_filename + '_ORG'):
        os.rename(nsi_filename, nsi_filename + '_ORG')
    with open(nsi_filename + '_ORG', 'r') as f:
        with open(nsi_filename, 'w') as f2: 
            f2.write('Unicode True\n')
            f2.write(f.read())

    # Make installer.
    if platform.system() == 'Windows':
        ret = os.system(
            "start /low /b /wait {bin_dir}\\NSIS\\makensis.exe {nsi_filename}".format(bin_dir=bin_dir, nsi_filename=nsi_filename))
    elif platform.system() == 'Linux':
        ret = os.system("makensis {nsi_filename}".format(nsi_filename=nsi_filename))
    else:
        raise Exception("Unsupported operating system.")
    if(ret == 0):
        print("Installer created.")
    else:
        raise Exception("NSIS compiler error.")
    
    # Move installer to the products directory.
    try:
        os.remove("{out_dir}/{map_name}-{wersja_mapy}.exe".format(
            out_dir=out_dir, map_version=map_version, map_name=map_name))
    except:
        pass
    os.rename("{map_name}.exe".format(map_name=map_name), "{out_dir}/{map_name}-{map_version}.exe".format(
        out_dir=out_dir, map_version=map_version, map_name=map_name))

    # Compress single Garmin IMG file.  
    if platform.system() == 'Windows':
        ret = os.system("start /low /b /wait {bin_dir}\\zip.exe -9 {out_dir}\\{map_name}-{map_version}_IMG.zip gmapsupp.img".format(
            bin_dir=bin_dir, map_version=map_version, out_dir=out_dir, map_name=map_name))
    elif platform.system() == 'Linux':
        ret = os.system("zip -9 {out_dir}/{map_name}-{map_version}_IMG.zip gmapsupp.img".format(
            binarki=bin_dir, map_version=map_version, out_dir=out_dir, map_name=map_name))
    else:
        raise Exception("Unsupported operating system.")

    if(ret == 0):
        print("ZIP archive containing gmapsupp.img created.")
    else:
        raise Exception("Blad kompresora ZIP")


def clean(mapa_root, map_work_dir):
    """Removes the working directory of map compilation.

    Args:
        mapa_root (string): path to a directory above map_work_dir
        map_work_dir (string): path to the directory to be removed
    """
    os.chdir(mapa_root)
    shutil.rmtree(map_work_dir, True)

