
 # HOW to build the image for testing and deploy in production
 ```
 sudo docker build -t IMAGE-NAME .
 sudo docker build -t main-python .
 ```

With the previous command in the it's possible to create the image, to run the command in the folder where the Dockerfile is present.


```
docker run -v PATH_TO_LOCAL_STORAGE:/files IMAGE-NAME string_dict_data [ENVIRONMENT_VAR]
sudo docker run -v /media/mithra/DISK/donwload_data:/files ghcr.io/tn-aixpa/sentinel-tools:0.3 "{'satelliteType': 'Sentinel1','startDate': '2023-12-12','endDate':'2023-12-13',  'processingLevel': 'LEVEL1',  'sensorMode': 'IW',  'productType': 'SLC',  'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))',  'area_sampling': 'False', 'artifact_name': 'directory_name_inside_s3',}" "{    'PROJECT_NAME':'',    'S3_ENDPOINT_URL':'',    'AWS_ACCESS_KEY_ID':'',    'AWS_SECRET_ACCESS_KEY':'',    'S3_BUCKET_NAME': 'prova',    'DIGITALHUB_CORE_ENDPOINT':'',     'CDSETOOL_ESA_USER':'',    'CDSETOOL_ESA_PASSWORD':''    }"
```
this command is used to test locally the image specifing the local volume which is going to be mounted to /files inside the image, IMAGE_NAME it's the name used during the build, string_dict_data it's the same string showed before in the code. Whith environment var it is possible to insert in the environment some parameters instead of specifing them on the ENV. This parameter can be passed as:
```
"""{
    'PROJECT_NAME':'',
    'S3_ENDPOINT_URL':'',
    'AWS_ACCESS_KEY_ID':'',
    'AWS_SECRET_ACCESS_KEY':'',
    'S3_BUCKET_NAME': 'prova',
    'DIGITALHUB_CORE_ENDPOINT':'', 
    'CDSETOOL_ESA_USER':'',
    'CDSETOOL_ESA_PASSWORD':''
    }"""
```
Those are parameters used in the digitalhub_core, CDSETOOL_ESA_USER and CDSETOOL_ESA_PASSWORD are also passed on the string_dict_data as user and password, later it will only be possible to pass through ENV.


# HOW to build the image for testing and deploy in production

In the near future just push on the release branch and it will be automated the release of the new version
