json_example = {
    "download": {
        "satelliteType": "Sentinel1",
        "startDate": "2023-12-24",
        "endDate": "2023-01-04",
        "processingLevel": "LEVEL1",
        "sensorMode": "IW",
        "productType": "IW_GRDH_1S",
        "geometry": "POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))",
        "path" : "/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/miao/bau",
        "user":"alattaruolo@fbk.eu",
        "password":"2CKb!#urVFbGUa4",
        "area_sampling": "False"
    },
    "processing": {}
}

json_for_sdk_example = {
    "PROJECT_NAME":"",
    "S3_ENDPOINT_URL":"",
    "AWS_ACCESS_KEY_ID":"",
    "AWS_SECRET_ACCESS_KEY":"",
    "S3_BUCKET_NAME": "",
    "DIGITALHUB_CORE_ENDPOINT":"",
}

"""{'download': {'satelliteType': 'Sentinel1', 'startDate': '2023-12-24', 'endDate': '2023-1-4', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'IW_GRDH_1S', 'geometry': 'POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))', 'path': '//media//dsl//1A2226C62D41B5A2//donwload_data//try_script//miao//bau', 'user': 'alattaruolo@fbk.eu', 'password': '2CKb!#urVFbGUa4'}, 'processing': {}}"""

"""{'satelliteType': 'Sentinel1', 'startDate': '2023-12-24', 'endDate': '2023-1-4', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'IW_GRDH_1S', 'geometry': 'POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))', 'path': '//media//dsl//1A2226C62D41B5A2//donwload_data//try_script//miao//bau', 'user': 'alattaruolo@fbk.eu', 'password': '2CKb!#urVFbGUa4'}"""

"""{'PROJECT_NAME':'my_project_sentinel','S3_ENDPOINT_URL':'http://172.17.0.2:9000','AWS_ACCESS_KEY_ID':'ROOTNAME','AWS_SECRET_ACCESS_KEY':'CHANGEME123','S3_BUCKET_NAME': 'prova','DIGITALHUB_CORE_ENDPOINT':''}"""

"""
'/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/docker'
# local execution
 python3.9 main.py "{'satelliteType': 'Sentinel1', 'startDate': '2023-12-24', 'endDate': '2023-01-04', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'IW_GRDH_1S', 'geometry': 'POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))', 'path': '/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/docker', 'user': 'alattaruolo@fbk.eu', 'password': 'aaa'}" "{'PROJECT_NAME':'my_project_sentinel','S3_ENDPOINT_URL':'http://172.17.0.2:9000','AWS_ACCESS_KEY_ID':'ROOTNAME','AWS_SECRET_ACCESS_KEY':'CHANGEME123','S3_BUCKET_NAME': 'prova','DIGITALHUB_CORE_ENDPOINT':''}"

"""

"""
docker build -t main-python .
docker run -v /media/dsl/1A2226C62D41B5A2/donwload_data/try_script/docker/:/files main-python  "{'satelliteType': 'Sentinel1', 'startDate': '2023-12-24', 'endDate': '2023-1-4', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'IW_GRDH_1S', 'geometry': 'POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))', 'path': 'files', 'user': 'alattaruolo@fbk.eu', 'password': 'aaa'}"
"""

"""
#environment varible in the run command
docker build -t main-python .
docker run -v /media/dsl/1A2226C62D41B5A2/donwload_data/try_script/docker/:/files  -e PROJECT_NAME='my_project_sentinel' -e S3_ENDPOINT_URL='http://172.17.0.3:9000' -e AWS_ACCESS_KEY_ID='ROOTNAME' -e AWS_SECRET_ACCESS_KEY='CHANGEME123' -e S3_BUCKET_NAME='prova' -e DIGITALHUB_CORE_ENDPOINT='' main-python  "{'satelliteType': 'Sentinel1', 'startDate': '2023-12-24', 'endDate': '2023-01-04', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'IW_GRDH_1S', 'geometry': 'POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))', 'path': 'files', 'user': 'alattaruolo@fbk.eu', 'password': 'aaa'}"
"""