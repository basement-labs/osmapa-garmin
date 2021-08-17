# osmapa-garmin

A complete environment setup for producing and sharing maps of Poland for Garmin GPS 
receivers using OpenStreetMap data, called OSMapaPL (available at https://garmin.osmapa.pl).

It consists of a toolchain (mkgmap, mkgmap styles, TYP files and helper scripts) used to compile 
maps, helper scripts to automate the process and code for a webpage to ditribute the maps.  

## Requirements for the toolchain

### Windows

1. Install Python 3.
2. Install Java.

All other tools are present in the `bin/` directory. 

### Linux

1. Install Python 3.
2. Install Java.
3. In addition to Python 3 and Java, additional tools must be available in the PATH:
    - `zip`
    - `osmconvert` and `osmfilter`
    - `nsis`

Here is how you can install all required components on a Ubuntu system:
```
apt install zip
apt install default-jre
apt install osmctools
apt install nsis
```

### Data files

Several required data files are not included in the git repo due to their size. You must fetch them 
manually and place in correct paths before running the toolchain. 

- `OSM/coastlines_europe-latest.osm.pbf`
- `OSM/srtm_polska.pbf`
- `bounds/*.bnd`  (http://osm.thkukuk.de/data/bounds-latest.zip)

## Usage

```python3 -u ProduceDistributionsPL.py```

## See also

See documentation in the `/doc/` directory.

## Main contributors

- Michał Rogala - Main project author
- Andrzej Talarczyk - Maintainer, main author of major rebuild - (@atalarczyk)
- Paweł Kosiorek - Visualization updates - (@dodoelk)

