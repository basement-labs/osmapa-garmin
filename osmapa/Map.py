"""OpenStreetMap map class. 

Author: Andrzej Talarczyk <andrzej@talarczyk.com>

License: GPLv3.
"""

import osmapa
import osmapa.get
import osmapa.boundaries
import osmapa.compile
import osmapa.split
import time

class Map:
    """Class representing a single Garmin map and the whole environment to generate it.
    """

    def __init__(self, version, fid, style, typfile, configfile, publisher_id, map_name, source_pbf_filename, root_dir, coastlinefile="", bounds_subdir="", lowercase=False, codepage="", verbose=False) -> None:
        self.version = version                                                          # wersja
        self.fid = fid                                                                  # fid_glowna
        self.style = style                                                              # styl_mapy_glowna
        self.typfile = typfile                                                          # typfile_glowna
        self.configfile = configfile
        self.source_pbf_filename = source_pbf_filename
        self.publisher_id = publisher_id                                                # 
        self.map_name = map_name                                                        #
        self.root_dir = root_dir                                                        # mapa_root
        self.coastlinefile = coastlinefile
        self.bounds_subdir = bounds_subdir
        self.lowercase = lowercase
        self.codepage = codepage
        self.verbose = verbose
        self.date = time.strftime('%Y%m%d')                                             # data_kompilacji

        self.map_id = self.publisher_id + self.fid + "001"
        self.map_version = self.date + self.version                                     # wersja_mapy
        self.bin_dir = self.root_dir + "/bin"                                           # binarki
        self.src_dir = self.root_dir + "/OSM"                                           # tmp_dane_osm
        self.work_dir = self.root_dir + "/tmp"                                          # katalog_tmp
        self.map_work_dir = self.work_dir + "/OSMapa-work-"  + self.map_version + "_" + self.publisher_id + self.fid    # tmp_mapa_glowna
        self.map_split_dir = self.work_dir + "/OSMapa-split-" + self.map_version + "_" + self.publisher_id + self.fid   # tmp_mapa_split_glowna
        self.out_dir = self.root_dir + "/products"                                    # mapy_gotowe


    def fetch(self, src_db_url, dest_filename) -> int:
        """Fetch source PBF data.

        Args:
            src_db_url (string): URL to the source PBF file.
            dest_filename (string): name under which the file will be saved

        Returns:
            int: status (0 - success)
        """        
        return osmapa.get.fetch_osm_data(bin_dir=self.bin_dir, url=src_db_url, dest_dir=self.src_dir, pbf_filename=dest_filename)


    def extract(self, src_filename, dest_filename, extract_polygon_filename) -> int:
        """Extract data from source_pbf_filename to extracted_pbf_filename by clipping with extract_polygon_filename.
        If extract_polygon_filename is an empty string, no extraction is done.   

        Args:
            src_filename (string): name of the file which should be clipped 
            dest_filename (string): name of clipped file will be saved
            extract_polygon_filename (string): path to a polygon file to be used as a mask for clipping

        Returns:
            int: 0 if success
        """
   
        if len(extract_polygon_filename) > 0:
            ret = osmapa.get.extract(bin_dir=self.bin_dir, work_dir=self.src_dir, source_pbf_filename=src_filename, extracted_pbf_filename=dest_filename, extract_polygon_filename=extract_polygon_filename)


    def generate_boundaries(self):
        """Generate boundaries for Poland. 

        Bugs:
            This method is not intended for general use.
        """
        osmapa.boundaries.generate(bin_dir=self.bin_dir, src_dir=self.src_dir, pbf_filename=self.source_pbf_filename)

    def split(self):
        """Split the map. 
        """
        osmapa.split.do(bin_dir=self.bin_dir, data_dir=self.src_dir, pbf_filename=self.source_pbf_filename, dest_dir=self.map_split_dir, map_id=self.map_id)

    def prepare(self):
        """Prepare compilation environment.
        """
        osmapa.compile.prepare(dest_dir=self.map_work_dir, split_source_dir=self.map_split_dir)

    def compile(self):
        """Compile the map.
        """
        osmapa.compile.produce(bin_dir=self.bin_dir, mapa_root=self.root_dir, map_work_dir=self.map_work_dir, typfile=self.typfile, style=self.style, configfile=self.configfile, fid=self.fid, src_dir=self.src_dir, map_version=self.map_version, publisher_id=self.publisher_id, map_name=self.map_name, out_dir=self.out_dir, coastlinefile=self.coastlinefile, bounds_subdir=self.bounds_subdir, lowercase=self.lowercase, codepage=self.codepage, verbose=self.verbose)

    def clean(self):
        """Clean up all temporary files used in the compilation process.
        """
        osmapa.split.clean(mapa_root=self.root_dir, split_dir=self.map_split_dir)
        osmapa.compile.clean(mapa_root=self.root_dir, map_work_dir=self.map_work_dir)

    def print_timestamped_message(self, msg):
        """Print out a message preceded with "==== OSMapa Generator", time stamp and map name.

        Args:
            msg (string): message text
        """
        print("==== OSMapa Generator [{time_str}]: {map_name} - {msg_str}".format(time_str=time.strftime('%Y-%m-%d %H:%M:%S'), map_name=self.map_name, msg_str=msg))
