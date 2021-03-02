# coding: utf-8
import os
from osmapa.Map import Map
import time

version = "V2.00"
src_db_url = "https://download.geofabrik.de/europe/poland-latest.osm.pbf"
# Alternate URL: https://download.openstreetmap.fr/extracts/europe/poland-latest.osm.pbf
polska_pbf_filename = 'poland-latest.osm.pbf'
srtm_pbf_filename = 'srtm_polska.pbf'
coastline_pbf_filename = 'coastlines_europe-latest.osm.pbf'
publisher_id = "66"
mapa_root = os.path.abspath("./")

if __name__ == "__main__":

        # OSMapaPL.

        mapGlowna = Map(version=version, source_pbf_filename=polska_pbf_filename, 
                publisher_id=publisher_id, root_dir=mapa_root, coastlinefile=coastline_pbf_filename,
                fid="004", 
                style="rogal",
                typfile="rogal.typ",
                configfile="osmapa.config",
                map_name="OSMapaPL-PODSTAWOWA", 
                bounds_subdir="bounds"
                )

        mapGlowna.print_timestamped_message("START.")
        
        # We fetch new map data only when processing the main map (OSMapaPL). Other maps use the same data. 
        mapGlowna.print_timestamped_message("Fetching new map data from the OSM server.")
        mapGlowna.fetch(src_db_url=src_db_url, dest_filename=polska_pbf_filename)

        mapGlowna.print_timestamped_message("Splitting.")
        mapGlowna.split()
        mapGlowna.print_timestamped_message("Preparing compilaton environment.")
        mapGlowna.prepare()
        mapGlowna.print_timestamped_message("Compiling.")
        mapGlowna.compile()
        mapGlowna.print_timestamped_message("Cleaning.")
        mapGlowna.clean()
        mapGlowna.print_timestamped_message("DONE.")

        # OSMapaPL-OGONKI.

        mapOgonki = Map(version=version, source_pbf_filename=polska_pbf_filename, 
                publisher_id=publisher_id, root_dir=mapa_root, coastlinefile=coastline_pbf_filename,
                fid="005", 
                style="rogal",
                typfile="rogal-ogonki.typ",
                configfile="osmapa_ogonki.config",
                map_name="OSMapaPL-OGONKI", 
                bounds_subdir="bounds", 
                lowercase=True,
                codepage="1250"
                )

        mapOgonki.print_timestamped_message("START.")
        mapOgonki.print_timestamped_message("Splitting.")
        mapOgonki.split()
        mapOgonki.print_timestamped_message("Preparing compilaton environment.")
        mapOgonki.prepare()
        mapOgonki.print_timestamped_message("Compiling.")
        mapOgonki.compile()
        mapOgonki.print_timestamped_message("Cleaning.")
        mapOgonki.clean()
        mapOgonki.print_timestamped_message("DONE.")

        # OSMapaPL-light.

        mapLight = Map(version=version, source_pbf_filename=polska_pbf_filename, 
                publisher_id=publisher_id, root_dir=mapa_root, coastlinefile=coastline_pbf_filename,
                fid="006", 
                style="osmapa-light",
                typfile="rogal.typ",
                configfile="osmapa_light.config",
                map_name="OSMapaPL-LIGHT", 
                bounds_subdir="bounds"
                )

        mapLight.print_timestamped_message("START.")
        mapLight.print_timestamped_message("Splitting.")
        mapLight.split()
        mapLight.print_timestamped_message("Preparing compilaton environment.")
        mapLight.prepare()
        mapLight.print_timestamped_message("Compiling.")
        mapLight.compile()
        mapLight.print_timestamped_message("Cleaning.")
        mapLight.clean()
        mapLight.print_timestamped_message("DONE.")

        # OSMapaPL-SZLAKI.

        mapSzlaki = Map(version=version, source_pbf_filename=polska_pbf_filename, 
                publisher_id=publisher_id, root_dir=mapa_root, 
                fid="011", 
                style="trasy-rowerowe",
                typfile="trasy-rowerowe.typ",
                configfile="osmapa_szlaki.config",
                map_name="OSMapaPL-SZLAKI"
                )

        mapSzlaki.print_timestamped_message("START.")
        mapSzlaki.print_timestamped_message("Splitting.")
        mapSzlaki.split()
        mapSzlaki.print_timestamped_message("Preparing compilaton environment.")
        mapSzlaki.prepare()
        mapSzlaki.print_timestamped_message("Compiling.")
        mapSzlaki.compile()
        mapSzlaki.print_timestamped_message("Cleaning.")
        mapSzlaki.clean()
        mapSzlaki.print_timestamped_message("DONE.")

        # OSMapaPL-WARSTWICE.

        mapWarstwice = Map(version=version, source_pbf_filename=srtm_pbf_filename, 
                publisher_id=publisher_id, root_dir=mapa_root, 
                fid="012", 
                style="osmapa-warstwice",
                typfile="",
                configfile="osmapa_warstwice.config",
                map_name="OSMapaPL-WARSTWICE"
                )

        mapWarstwice.print_timestamped_message("START.")
        mapWarstwice.print_timestamped_message("Splitting.")
        mapWarstwice.split()
        mapWarstwice.print_timestamped_message("Preparing compilaton environment.")
        mapWarstwice.prepare()
        mapWarstwice.print_timestamped_message("Compiling.")
        mapWarstwice.compile()
        mapWarstwice.print_timestamped_message("Cleaning.")
        mapWarstwice.clean()
        mapWarstwice.print_timestamped_message("DONE.")
