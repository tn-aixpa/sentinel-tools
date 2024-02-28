from pathlib import Path
import os
from zipfile import ZipFile
import geojson
import json
from shapely.geometry import shape
import shapely.wkt

def create_path(path,name):
    return os.path.join(path,name)

def get_path_geojson():
    return create_path("data","geojson_area.geojson")

def get_path_geometry_burst():
    return create_path("assets","sarmpc_s1_burstid_v20220530_iw_merged.geojson")

def get_path_geometry_mgrs():
    return create_path("assets","sentinel2_mgrs_tiles_world.geojson")
def get_path_snap_coherence():
    return create_path("assets","s1coherence.xml")
def fromSAFE_toZIP(filename: str):
    """
    rename file custom 
    """
    return filename.replace(".SAFE",".zip")

def unzipFile(zipFile: str,newPath: str):
    """
    unzip a file in the path provided 
    """
    with ZipFile(zipFile, 'r') as zObject:
        zObject.extractall(newPath)

def unzipDownload(filename:str):
    """
    unzip a file 
    """
    try:
        zipFile = fromSAFE_toZIP(filename)
        print(zipFile)
        if os.path.exists(zipFile):
            # not unzipped yet
            path = Path(filename)
            parentDir = path.parent.absolute()
            unzipFile(zipFile,parentDir)
            #deleteFile(zipFile)
            print(f"{filename} unzipped!")
    except Exception as e:
        print(f"Error while unzipping file {filename}")

def get_all_files_name_in_dir(dir_name:str):
    """
    Get all files names in a directory, just files no folder
    """
    return os.listdir(dir_name)

def from_geojson_to_file(json_obj,path="data",name="geojson_area.geojson"):
    """
    Creates a geojson file inside the path with name by default in data/geojson_area.geojson
    """
    full_dir_path_with_name = os.path.join(path,name)
    try:
        with open(full_dir_path_with_name, 'w') as outfile:
            json.dump(json_obj, outfile)
        return full_dir_path_with_name
    except Exception as e:
        print("Create geojson error:", e)
        return ""

def from_wkt_to_geojson(wkt):
    """
    Given a wkt return the geojson
    """
    g1 = shapely.wkt.loads(wkt)
    g2 = geojson.Feature(geometry=g1, properties={})
    return g2.geometry

def from_geojson_to_wkt(obj):
    """
    Given a geojson return a wkt
    """
    g2 = shape(obj)
    return g2.wkt

def remover_all_files_from_directory(path):
    pass