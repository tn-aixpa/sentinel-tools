
import json
from cdsetool.query import query_features, shape_to_wkt,describe_collection
from cdsetool.credentials import Credentials
from cdsetool.monitor import StatusMonitor
from cdsetool.download import download_features
from util.geometry_modifier import get_bursts,get_mgrs
from datetime import date

from util.input_sentinel_class import InputSentinelClass

def download_from_object_json(obj: InputSentinelClass):
    download(obj.satelliteType,obj.startDate,obj.endDate,obj.processingLevel,obj.sensorMode,obj.productType,obj.geometry,obj.path,obj.user,obj.password)
    
def download(satelliteType,startDate,endDate,processingLevel,sensorMode,productType,geometry,path,user,password):
    features = query_features(
    satelliteType,
    {
        "startDate": startDate,
        'status':     'ONLINE',
        "completionDate": endDate,
        "processingLevel": processingLevel,
        "sensorMode": sensorMode,
        "productType": productType,
        "geometry": geometry#shape_to_wkt("/home/dsl/Documents/fbk/CDSETool/tests/shape/POLYGON.shp"),
    },
    )
    for feature in features:
        print(feature.get("properties").get("title"))
    list(
    download_features(
        features,
        path,
        {
            "concurrency": 4,
            "monitor": StatusMonitor(),
            "credentials": Credentials(user, password),
        },
    )
)

def from_string_to_json(string):
    return json.loads(string)

def from_json_to_string(json_object):
    return json.dumps(json_object)

