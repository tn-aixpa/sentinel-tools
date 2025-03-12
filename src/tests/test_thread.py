import sys
import json
from util.input_sentinel_class import InputSentinelClass
from util.helper import from_geojson_to_file, from_wkt_to_geojson,get_path_geojson, get_path_geometry_burst,get_path_geometry_mgrs,create_path, remover_all_files_from_directory
from util.geometry_modifier import get_bursts,get_bust_second,get_mgrs
from util.cdsetool_handler_burst_mgs import download_products_new, get_query_sentinel1,download_products
from util.preprocess_sentinel_1 import coherence_snap_cmds
from util.command_execution import CommandExecution
from threading import Thread
from cdsetool.query import query_features
from cdsetool.credentials import Credentials
from cdsetool.download import download_features
from cdsetool.monitor import StatusMonitor

def from_string_to_json(string):
    return json.loads(string)

def execution():
    collection = 'Sentinel1'
    search_terms = {'orbitDirection': 'ASCENDING', 'relativeOrbitNumber': 15, 'geometry': 'POINT(10.637208711454361 45.401959349421986)', 'sortOrder': 'asc', 'sortParam': 'startDate', 'status': 'ONLINE', 'startDate': '2023-12-01T00:00:00.000Z', 'completionDate': '2023-12-13T23:59:59.999Z', 'productType': 'SLC', 'sensorMode': 'IW', 'processingLevel': 'LEVEL1'}
    #query products features
    features = query_features(collection, search_terms)
    credentials = Credentials("","")
    options = {'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
    #options = {"tmpdir": products_dir,'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
    list(download_features(features, "/home/mithra/Documents/donwload_sentinel_test/", options))
    
if __name__ == "__main__":
    t = Thread(target=execution, args=[1])
    t.run()
# sudo docker build -t test-python .
# sudo docker run -v /home/mithra/Documents/donwload_sentinel_test/:/files test-python