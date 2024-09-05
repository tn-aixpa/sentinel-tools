import sys
import json
from util.input_sentinel_class import InputSentinelClass
from util.helper import from_geojson_to_file, from_wkt_to_geojson,get_path_geojson, get_path_geometry_burst,get_path_geometry_mgrs,create_path, remover_all_files_from_directory
from util.geometry_modifier import get_bursts,get_bust_second,get_mgrs
from util.cdsetool_handler_burst_mgs import download_products_new, get_query,download_products
from util.preprocess_sentinel_1 import coherence_snap_cmds
from util.command_execution import CommandExecution

def from_string_to_json(string):
    return json.loads(string)

if __name__ == "__main__":
    abc = """{
  'satelliteType': 'Sentinel1',
  'startDate': '2023-12-12',
  'endDate': '2023-12-13',
  'processingLevel': 'LEVEL1',
  'sensorMode': 'IW',
  'productType': 'SLC',
  'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))',
  'area_sampling': 'True',
  'artifact_name': 'files_from_sentinel'
  }"""
    corret_form = abc.replace("'","\"")
    json_input_download = from_string_to_json(corret_form)
    user,password = "alattaruolo@fbk.eu","2CKb!#urVFbGUa4"
    download_parameters = InputSentinelClass(json_input_download,user=user,password=password)
    geoj = from_wkt_to_geojson(download_parameters.geometry)
    from_geojson_to_file(geoj)
    download_parameters.embed_parameters_preprocessing_sentienl1()
    path_geojson = get_path_geojson()
    path_burst = get_path_geometry_burst()
    df = get_bursts(path_geojson,path_burst)
    query_df,features = get_query(df,download_parameters)
    #DOWNLOAD_PATH = "/home/mithra/Documents/donwload_sentinel_test/"
    DOWNLOAD_PATH = "/media/mithra/DISK/donwload_data/"
    download_products(query_df,DOWNLOAD_PATH,download_parameters.user,download_parameters.password,download_parameters.tmp_path_same_folder_dwl)
    print("PREPROCESSING STARTED ...")
    PREPROCESS_PATH = "preprocessed"
    preprocess_path = create_path(DOWNLOAD_PATH,PREPROCESS_PATH)
    snap_commands = coherence_snap_cmds(query_df,DOWNLOAD_PATH,preprocess_path)
    print(f"finished download {snap_commands}",)
    exectuionenr = CommandExecution(snap_commands)
    exectuionenr.execute()
    print("Command executed")